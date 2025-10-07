##############################################################################
# pipeline/adapters.py — Provider dispatcher
# Central place to:
#   • Read GEN_PROVIDER from env (or brief)
#   • Route to the correct provider impl (sdxl, stability, firefly, placeholder)
##############################################################################
import os
from typing import Optional, Dict, Any
from PIL import Image

# Import provider modules (each isolates its own dependencies)
from .providers import sdxl_diffusers, stability_api, firefly_api

def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    """Helper to read environment variables with a default."""
    return os.environ.get(name, default)

def choose_provider(name: Optional[str]) -> str:
    """Resolve provider from explicit name → env → default."""
    n = (name or _env("GEN_PROVIDER") or "placeholder").strip().lower()
    if n in {"sdxl", "stability", "firefly", "placeholder"}:
        return n
    return "placeholder"

def generate_with_provider(
    provider: str, w: int, h: int, product_name: str, hint: str, params: Dict[str, Any]
) -> Image.Image:
    """Call into the chosen provider module."""
    if provider == "sdxl":
        return sdxl_diffusers.generate(w, h, product_name, hint, params=params)
    elif provider == "stability":
        return stability_api.generate(w, h, product_name, hint, params=params)
    elif provider == "firefly":
        return firefly_api.generate(w, h, product_name, hint, params=params)
    else:
        # Default local placeholder (no network, no heavy deps)
        from .fallback_placeholder import generate_fallback
        return generate_fallback(w, h, product_name, hint)
