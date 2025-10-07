#!/usr/bin/env python3
##############################################################################
# app.py — CLI entrypoint
# Purpose:
#   - Load a campaign brief (YAML/JSON)
#   - Generate creatives per product × aspect_ratio × market
#   - Run legal + brand checks
#   - Emit a CSV report and organized folder outputs
#
# Interview notes:
#   • Keep this file small and readable; push complexity into pipeline modules.
#   • The only "smart" logic here is brief parsing and orchestration.
##############################################################################

import sys, os, json                               # stdlib: CLI args, filesystem, JSON
from typing import Dict, Any                       # typing for clarity (optional)
from PIL import Image                              # image IO (only used if asset provided)
import yaml                                        # YAML brief support

# Local modules that encapsulate responsibilities
from pipeline.generators import generate_image     # provider-agnostic image generation
from pipeline.layout import render_creative        # text/brand/logo composition
from pipeline.brand_checks import run_brand_checks # simple palette/size/logo checks
from pipeline.legal_checks import run_legal_checks # prohibited-term flags
from pipeline.reporting import Reporter            # CSV run log

# Fixed output sizes per aspect ratio (Instagram/TikTok/YouTube-friendly).
ASPECT_MAP = {
    "1:1": (1080, 1080),   # Square
    "9:16": (1080, 1920),  # Vertical
    "16:9": (1920, 1080),  # Horizontal
}

def load_brief(path: str) -> Dict[str, Any]:
    """Load a YAML or JSON brief. Keep format flexible for teams."""
    with open(path, "r") as f:                     # open the file once
        if path.endswith(".json"):                 # JSON path
            return json.load(f)                    # parse as JSON
        return yaml.safe_load(f)                   # else parse as YAML

def main():
    # --- CLI guard + parse ---
    if len(sys.argv) < 2:                          # require a path argument
        print("Usage: python app.py <brief.yaml|brief.json>")
        sys.exit(1)

    brief_path = sys.argv[1]                       # first CLI arg is the brief path
    brief = load_brief(brief_path)                 # parse into a dict

    # --- Pull strongly-typed fields from the brief with sensible defaults ---
    campaign = brief.get("campaign_name", "campaign")
    products = brief.get("products", [])           # expect >=2 products
    aspect_ratios = brief.get("aspect_ratios", ["1:1", "9:16", "16:9"])
    out_root = brief.get("output_dir", "output")
    markets = brief.get("target_markets", ["US"])
    messages = brief.get("campaign_message", {"en": "Hello World"})
    palette = brief.get("brand_palette", {"primary_hex": "#0B0B0B", "accent_hex": "#FFD700"})
    logo_path = brief.get("brand_logo_path")
    prohibited = brief.get("legal_prohibited_words", [])

    if len(products) < 2:                          # simple requirement check
        raise SystemExit("Brief must include at least two products.")

    # Pre-create the campaign root folder and attach the CSV reporter
    campaign_dir = os.path.join(out_root, campaign)
    os.makedirs(campaign_dir, exist_ok=True)
    reporter = Reporter(os.path.join(campaign_dir, "run_report.csv"))

    # --- Main nested loops: product × aspect_ratio × market ---
    for product in products:
        pid = product["id"]                        # required
        pname = product.get("name", pid)           # display name
        hint = product.get("asset_hint", "")       # textual hint for the generator
        input_image = product.get("input_image")   # optional existing asset path

        for ar in aspect_ratios:
            if ar not in ASPECT_MAP:               # guard unknown ratios
                print(f"[warn] Unknown aspect ratio {ar}, skipping.")
                continue

            w, h = ASPECT_MAP[ar]                  # map ratio to exact pixel size

            for market in markets:
                # Map market → language key for localized message
                lang_key = "en"
                ml = market.lower()
                if ml in ("de", "germany"): lang_key = "de"
                elif ml in ("jp", "japan"): lang_key = "ja"

                message = messages.get(lang_key, messages.get("en", ""))

                # Prepare output directory
                out_dir = os.path.join(campaign_dir, pid, ar, market)
                os.makedirs(out_dir, exist_ok=True)

                # Read generator preferences (provider + params) from the brief
                gen_cfg = (brief.get('generator') or {})
                provider = gen_cfg.get('provider')         # placeholder | sdxl | stability | firefly
                gen_params = gen_cfg.get('params') or {}   # e.g., prompt template, steps, etc.

                # --- Source image: reuse if provided; otherwise generate on the fly ---
                if input_image and os.path.exists(input_image):
                    base = Image.open(input_image).convert("RGB").resize((w, h))
                    source = "provided_asset"
                else:
                    base = generate_image(
                        w, h, pname, hint,
                        provider_name=provider, params=gen_params
                    )
                    source = f"generated:{provider or 'auto'}"

                # Compose brand panel + logo over the base image
                composed = render_creative(
                    base_img=base,
                    message=message,
                    brand_logo_path=logo_path,
                    brand_palette=palette
                )

                # Persist creative to disk (organized path for approvals)
                fn = f"{pid}_{ar}_{market}.png"
                out_path = os.path.join(out_dir, fn)
                composed.save(out_path)

                # Run checks and write to the CSV report for reviewers
                legal_flags = run_legal_checks(message, prohibited)
                brand_flags = run_brand_checks(
                    out_path,
                    logo_present=bool(logo_path),
                    expected_size=(w, h),
                    palette=palette
                )

                reporter.write({
                    "campaign": campaign,
                    "product_id": pid,
                    "product_name": pname,
                    "market": market,
                    "aspect_ratio": ar,
                    "source_image": source,
                    "output_path": out_path,
                    "legal_flags": "|".join(legal_flags) if legal_flags else "",
                    "brand_flags": "|".join(brand_flags) if brand_flags else "",
                })

                print(f"[ok] {out_path} (legal={legal_flags}, brand={brand_flags})")

    print(f"\nAll done. Review report: {os.path.join(campaign_dir, 'run_report.csv')}")

if __name__ == "__main__":
    main()
