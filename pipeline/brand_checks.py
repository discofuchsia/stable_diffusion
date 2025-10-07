##############################################################################
# pipeline/brand_checks.py — Cheap, fast checks for demo purposes
# Checks:
#   • exact output size match for the chosen aspect ratio
#   • presence of the accent color (approximate sampling)
#   • logo presence flag (based on path provided)
##############################################################################
from typing import List, Tuple, Dict
from PIL import Image

def _hex_to_rgb(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0,2,4))

def run_brand_checks(image_path: str, logo_present: bool, expected_size: Tuple[int,int], palette: Dict[str,str]) -> List[str]:
    flags = []

    with Image.open(image_path) as im:
        # 1) Exact size check — catches accidental resizes
        if im.size != expected_size:
            flags.append(f"unexpected_size:{im.size}!={expected_size}")

        # 2) Accent color presence — sample a coarse grid to keep it fast
        accent = _hex_to_rgb(palette.get("accent_hex", "#FFD700"))
        w, h = im.size
        hit = False
        for x in range(0, w, max(1, w//20)):
            for y in range(0, h, max(1, h//20)):
                r,g,b = im.getpixel((x,y))[:3]
                if abs(r - accent[0]) < 30 and abs(g - accent[1]) < 30 and abs(b - accent[2]) < 30:
                    hit = True
                    break
            if hit: break
        if not hit:
            flags.append("accent_not_detected")

    # 3) If no logo path was provided, raise a flag (simple but useful)
    if not logo_present:
        flags.append("logo_missing")

    return flags
