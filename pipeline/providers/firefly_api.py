##############################################################################
# providers/firefly_api.py — Placeholder Firefly adapter
# Notes:
#   • Stubbed to keep base repo lightweight and avoid external dependencies.
#   • Replace with the actual Firefly call in your environment.
##############################################################################
from typing import Dict, Any
from PIL import Image, ImageDraw
import os
from ..fallback_placeholder import generate_fallback

def generate(w: int, h: int, product_name: str, hint: str, params: Dict[str, Any]) -> Image.Image:
    api_key = os.environ.get("FIREFLY_API_KEY") or params.get("api_key")
    if not api_key:
        raise RuntimeError("Firefly provider requested but FIREFLY_API_KEY missing.")

    # For now, return a fallback image with a small label so reviewers can see the path
    img = generate_fallback(w, h, product_name, hint)
    d = ImageDraw.Draw(img)
    d.text((10, 10), "Firefly (stub)", fill=(0, 0, 255))
    return img
