##############################################################################
# pipeline/generators.py — Provider-agnostic generate_image()
# This is the public function the app calls; it picks a provider and
# gracefully falls back to a placeholder if the provider fails.
##############################################################################
from PIL import Image
from typing import Dict, Any
from .adapters import choose_provider, generate_with_provider

def generate_image(
    w: int,
    h: int,
    product_name: str,
    hint: str,
    provider_name: str = None,
    params: Dict[str, Any] = None
) -> Image.Image:
    """Select a provider (env or brief) and generate an image.

    Args:
        w,h: Output canvas in pixels.
        product_name: For prompt or on-image label.
        hint: Textual description (lights, style, etc.).
        provider_name: Optional override ('placeholder'|'sdxl'|'stability'|'firefly').
        params: Provider-specific knobs (prompt_template, steps, cfg, seed).

    Returns:
        PIL.Image.Image of size (w,h).
    """
    provider = choose_provider(provider_name)      # resolve final provider
    try:
        return generate_with_provider(
            provider, w, h, product_name, hint, params or {}
        )
    except Exception as e:
        # Any provider error → fallback image, with a visible on-canvas reason.
        from .fallback_placeholder import generate_fallback
        img = generate_fallback(w, h, product_name, hint)
        from PIL import ImageDraw
        d = ImageDraw.Draw(img)
        d.text((10, 10), f"{provider} failed: {e}", fill=(255, 0, 0))
        return img
