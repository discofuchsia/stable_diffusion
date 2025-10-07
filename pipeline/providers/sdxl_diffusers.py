##############################################################################
# providers/sdxl_diffusers.py — Local SDXL via HuggingFace Diffusers (optional)
# Notes:
#   • This requires torch + diffusers; keep it optional behind requirements-extras.
#   • In the interview: call out that the rest of the code runs without these deps.
##############################################################################
from typing import Dict, Any
from PIL import Image

# Optional heavy imports — guarded so the base repo stays light
try:
    from diffusers import StableDiffusionXLPipeline
    import torch
    _HAS_DIFFUSERS = True
except Exception as e:
    _HAS_DIFFUSERS = False
    _IMPORT_ERR = e

def _build_prompt(product_name: str, hint: str, params: Dict[str, Any]) -> str:
    """Small prompt helper so we can swap templates centrally."""
    tmpl = params.get("prompt_template") or "{name}: {hint}, studio lighting, product photography, high detail"
    return tmpl.format(name=product_name, hint=hint)

def generate(w: int, h: int, product_name: str, hint: str, params: Dict[str, Any]) -> Image.Image:
    if not _HAS_DIFFUSERS:
        # Fail with a readable message that the caller will paint onto a fallback image.
        raise RuntimeError(f"SDXL provider requested but diffusers/torch not installed: {_IMPORT_ERR}")

    prompt = _build_prompt(product_name, hint, params or {})

    # Load a public SDXL base checkpoint (can be swapped for internal models)
    pipe = StableDiffusionXLPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0")

    # Auto-select device; works on CPU, but GPU is recommended
    device = "cuda" if torch.cuda.is_available() else "cpu"
    pipe = pipe.to(device)

    # Keep params conservative to fit demo time
    out = pipe(
        prompt=prompt,
        width=w, height=h,
        guidance_scale=params.get("guidance_scale", 5.0),
        num_inference_steps=params.get("steps", 25),
    ).images[0]

    return out
