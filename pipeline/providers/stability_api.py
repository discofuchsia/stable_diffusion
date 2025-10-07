# pipeline/providers/stability_api.py
from typing import Dict, Any, Optional, Tuple
from PIL import Image
import os, requests, base64, io

# ------------------------------ helpers ------------------------------

def _build_prompt(product_name: str, hint: str, params: Dict[str, Any]) -> str:
    tmpl = (params or {}).get("prompt_template") or "{name}: {hint}, studio lighting, product photography, high detail"
    return tmpl.format(name=product_name, hint=hint or "")

def _ensure_canvas(w: int, h: int) -> Tuple[int, int]:
    # keep incoming canvas sane for non-SDXL paths
    tw = max(256, (w // 8) * 8)
    th = max(256, (h // 8) * 8)
    return tw, th

# Allowed SDXL v1 sizes (width, height)
_SDXL_V1_ALLOWED = [
    (1024, 1024),
    (1152,  896), (1216,  832), (1344,  768), (1536,  640),
    ( 640, 1536), ( 768, 1344), ( 832, 1216), ( 896, 1152),
]

def _sdxl_dims_whitelist(w: int, h: int) -> Tuple[int, int]:
    """
    Choose the closest SDXL v1-allowed size to (w,h), preserving orientation
    when possible; fall back to the full set for near-square.
    """
    if w <= 0 or h <= 0:
        return (1024, 1024)
    target_ratio = w / h
    landscape = w >= h
    candidates = [(W, H) for (W, H) in _SDXL_V1_ALLOWED if (W >= H) == landscape]
    if not candidates or abs(target_ratio - 1.0) < 1e-3:
        candidates = _SDXL_V1_ALLOWED
    best = min(
        candidates,
        key=lambda WH: (abs((WH[0]/WH[1]) - target_ratio), abs(WH[0] - w) + abs(WH[1] - h))
    )
    return best

# ------------------------------ v1 (SDXL) ------------------------------

def _legacy_sdxl(host: str, api_key: str, prompt: str, width: int, height: int, params: Dict[str, Any]) -> Image.Image:
    url = f"{host}/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "image/png",
        "Content-Type": "application/json",
    }
    payload = {
        "text_prompts": [{"text": prompt}],
        "cfg_scale": params.get("guidance_scale", 5.0),
        "height": height,
        "width": width,
        "samples": 1,
        "steps": params.get("steps", 28),
        # "seed": params.get("seed"),
    }
    resp = requests.post(url, json=payload, headers=headers, timeout=120)
    if not resp.ok:
        raise RuntimeError(f"Stability v1 SDXL error: {resp.status_code} {resp.text}")
    return Image.open(io.BytesIO(resp.content)).convert("RGB")

# ------------------------------ v2beta (core/sd3/etc.) ------------------------------

def _json_core(host: str, engine: str, api_key: str, prompt: str, width: int, height: int, params: Dict[str, Any]) -> Image.Image:
    url = f"{host}/v2beta/stable-image/generate/{engine}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = {
        "prompt": prompt,
        "output_format": "png",
        "width": width,
        "height": height,
        "seed": params.get("seed"),
        "cfg_scale": params.get("guidance_scale", 5.0),
        "steps": params.get("steps", 25),
    }
    resp = requests.post(url, json=payload, headers=headers, timeout=120)
    if not resp.ok:
        raise requests.HTTPError(f"{resp.status_code} {resp.text}", response=resp)
    data = resp.json()
    b64 = data.get("image") or (data.get("images") or [{}])[0].get("image")
    if not b64:
        raise RuntimeError("Stability API (json): no image in response.")
    raw = base64.b64decode(b64)
    return Image.open(io.BytesIO(raw)).convert("RGB")

def _multipart_core(host: str, engine: str, api_key: str, prompt: str, width: int, height: int, params: Dict[str, Any]) -> Image.Image:
    url = f"{host}/v2beta/stable-image/generate/{engine}"
    headers = {"Authorization": f"Bearer {api_key}", "Accept": "image/png"}
    form = {
        "prompt": (None, prompt),
        "output_format": (None, "png"),
        "width": (None, str(width)),
        "height": (None, str(height)),
    }
    if "seed" in params: form["seed"] = (None, str(params["seed"]))
    if "guidance_scale" in params: form["cfg_scale"] = (None, str(params["guidance_scale"]))
    if "steps" in params: form["steps"] = (None, str(params["steps"]))
    resp = requests.post(url, files=form, headers=headers, timeout=120)
    if not resp.ok:
        raise requests.HTTPError(f"{resp.status_code} {resp.text}", response=resp)
    return Image.open(io.BytesIO(resp.content)).convert("RGB")

# ------------------------------ main entry ------------------------------

def generate(w: int, h: int, product_name: str, hint: str, params: Dict[str, Any]) -> Image.Image:
    """
    Unified generator:
      - SDXL-like engines -> v1 SDXL (snap to allowed dims), then resize to (w,h)
      - Otherwise v2beta JSON → multipart; fallback to v1 SDXL
    """
    api_key = os.environ.get("STABILITY_API_KEY") or (params or {}).get("api_key")
    if not api_key:
        raise RuntimeError("Stability provider requested but STABILITY_API_KEY missing.")

    host = (os.environ.get("STABILITY_API_HOST", "https://api.stability.ai")).rstrip("/")
    engine = os.environ.get("STABILITY_ENGINE", (params or {}).get("engine") or "stable-image-core")

    prompt = _build_prompt(product_name, hint, params or {})
    target_W, target_H = w, h
    w, h = _ensure_canvas(w, h)

    # SDXL engines -> v1 route with whitelist dims
    if engine.startswith("stable-diffusion-xl-") or engine.startswith("sdxl"):
        sdxl_w, sdxl_h = _sdxl_dims_whitelist(w, h)
        img = _legacy_sdxl(host, api_key, prompt, sdxl_w, sdxl_h, params or {})
        if img.size != (target_W, target_H):
            img = img.resize((target_W, target_H))
        return img

    # v2beta JSON first
    try:
        return _json_core(host, engine, api_key, prompt, w, h, params or {})
    except requests.HTTPError as e:
        code = getattr(e, "response", None).status_code if getattr(e, "response", None) else None
        if code not in (404, 415):
            raise

    # v2beta multipart
    try:
        return _multipart_core(host, engine, api_key, prompt, w, h, params or {})
    except requests.HTTPError as e:
        code = getattr(e, "response", None).status_code if getattr(e, "response", None) else None
        if code != 404:
            raise

    # final fallback to SDXL v1
    sdxl_w, sdxl_h = _sd_
