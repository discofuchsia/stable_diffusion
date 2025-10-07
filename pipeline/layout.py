##############################################################################
# pipeline/layout.py — Brand-safe composition: message panel + logo placement
##############################################################################
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, Optional
import os

def _load_font(size: int):
    """Try to load a TTF; fallback to PIL's default so the demo never breaks."""
    try:
        return ImageFont.truetype("arial.ttf", size=size)
    except:
        return ImageFont.load_default()

def render_creative(base_img: Image.Image, message: str, brand_logo_path: Optional[str], brand_palette: Dict[str,str]) -> Image.Image:
    # Work on a copy in RGBA so we can alpha-compose
    img = base_img.copy().convert("RGBA")
    w, h = img.size
    draw = ImageDraw.Draw(img)

    # Use accent color for headline; keep background panel semi-opaque
    accent = brand_palette.get("accent_hex", "#FFD700")

    # Message panel geometry — proportionate to the canvas so it scales with size
    pad = int(min(w, h) * 0.04)
    box_h = int(h * 0.22)
    draw.rounded_rectangle([pad, h - box_h - pad, w - pad, h - pad], radius=24, fill=(0,0,0,180))

    # Headline text
    font = _load_font(int(min(w, h) * 0.055))
    draw.text((pad*1.4, h - box_h), message, fill=accent, font=font)

    # Logo in the bottom-right; scaled to ~18% width
    if brand_logo_path and os.path.exists(brand_logo_path):
        logo = Image.open(brand_logo_path).convert("RGBA")
        logo_w = int(w * 0.18)
        ratio = logo_w / logo.width
        logo_h = int(logo.height * ratio)
        logo = logo.resize((logo_w, logo_h))
        img.alpha_composite(logo, (w - logo_w - pad, h - logo_h - pad))

    # Return final RGB (no alpha) for cross-platform compatibility
    return img.convert("RGB")
