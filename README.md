# 🎨 Creative Automation Pipeline (POC)

**Author:** [Jules Gerard](https://github.com/discofuchsia)

✨ Author

Jules Gerard — Generative AI Engineer & Creative Technologist

GitHub: @discofuchsia

LinkedIn: linkedin.com/in/jules-gerard-ai23

Email: discofuchsia@gmail.com

"Blending design intuition with machine intelligence — building the next generation of creative tools."

**Focus:** Generative AI · Creative Automation · Python · Stability AI SDXL · ComfyUI · Brand Intelligence

> "Turning briefs into brand-perfect visuals — automatically."

---

## 🚀 Overview

This is a **Creative Automation Proof of Concept** — a production-style pipeline that converts structured campaign briefs into brand-compliant, AI-generated visuals using **Stable Diffusion XL**, **ComfyUI**, and **Python**.

It demonstrates how generative AI platforms can scale content generation for global marketing teams through automation, localization, and brand enforcement.

> Imagine campaign assets updating themselves overnight — consistent, compliant, and creative.
> This repo makes that vision real in code.

---

## 🧠 Core Capabilities

| Capability | Description |
| --- | --- |
| 🧩 **Automated Asset Generation** | Reads YAML briefs and auto-generates images per product, market, and ratio. |
| 🎨 **Stable Diffusion SDXL Integration** | Direct API calls to Stability AI's SDXL v1 endpoint with intelligent dimension snapping. |
| 🖼️ **Dynamic Layout Engine** | Adds brand text, palette accents, and logos using Pillow. |
| ✅ **Brand & Legal QA** | Runs automated compliance checks for palette and prohibited words. |
| 🧾 **Structured Outputs** | Generates a consistent folder structure and CSV report for QA. |
| ⚙️ **Smart Error Handling** | Automatically adapts illegal SDXL dimensions and resizes cleanly. |
| 🧪 **Commented Codebase** | Every file includes detailed commentary for walkthroughs. |

---

## 🏗️ Architecture

```
stable_diffusion/
├── app.py                    # CLI entry point
├── briefs/sample_brief.yaml  # Example marketing brief
├── assets/
│   ├── logos/brand_logo.png
│   └── products/
├── pipeline/
│   ├── generators.py
│   ├── adapters.py
│   ├── providers/
│   │   ├── stability_api.py    # SDXL v1 + v2beta engines
│   │   └── sdxl_diffusers.py   # Local Diffusers integration
│   ├── layout.py
│   ├── brand_checks.py
│   ├── legal_checks.py
│   └── reporting.py
├── demo.sh                   # One-command demo
├── VIDEO_DEMO_GUIDE.md       # 2–3 min narration guide
└── README.md                 # (this file)
```

---

## 💡 Vision

Creative teams waste hours generating endless ad variations.
This project blends **AI creativity** with **brand control**, automating asset creation while keeping every output on-brand.

Built for:

* **Generative design workflows at scale**
* **Responsible, brand-safe AI content**
* **Automated localization & multi-market scaling**

---

## ⚙️ Quickstart

### 1️⃣ Environment Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-extras.txt
```

### 2️⃣ Run the Demo

```bash
bash demo.sh
```

or manually:

```bash
python app.py briefs/sample_brief.yaml
```

### 3️⃣ Output Example

```
output/
└── Autumn Launch/
    ├── sku-espresso-01/
    │   ├── 1:1/US/sku-espresso-01_1:1_US.png
    │   ├── 9:16/DE/sku-espresso-01_9:16_DE.png
    │   └── 16:9/JP/sku-espresso-01_16:9_JP.png
    ├── sku-grinder-02/
    └── run_report.csv
```

Each asset includes:

- Localized message
- Brand palette overlay
- Logo placement
- Automatic metadata logging

---

## 🧬 Stability AI Setup

```bash
export STABILITY_API_HOST=https://api.stability.ai
export STABILITY_API_KEY=sk-yourkey
export STABILITY_ENGINE=stable-diffusion-xl-1024-v1-0
```

The pipeline auto-snaps to SDXL's legal resolutions (e.g. 1344×768, 768×1344, 1024×1024) and resizes back to your target canvas for flawless output.

---

## 🧑‍💻 Code Walkthrough

| File | Talking Points |
| --- | --- |
| `app.py` | Orchestrates brief parsing and generation flow. |
| `pipeline/generators.py` | Decides which provider to use and handles fallbacks. |
| `providers/stability_api.py` | Integrates SDXL v1 + v2beta APIs, handling legal sizes and retries. |
| `layout.py` | Handles creative composition — text and brand placement. |
| `brand_checks.py` | Validates logo, palette, and compliance. |
| `reporting.py` | Logs all creative data to CSV for QA. |

---

## 🎥 Demo Video

Record or build a 2–3 minute demo following `VIDEO_DEMO_GUIDE.md`.

Scenes:

1. YAML brief + terminal run
2. SDXL generation in action
3. Output folder + sample creatives
4. CSV report summary
5. Outro with your GitHub link

🎬 "From YAML to final asset — AI-driven Creative Automation."

---

## 🧩 Roadmap

- 🔗 Integrate ComfyUI node-based workflows for advanced img2img and ControlNet pipelines
- 🧱 Add Streamlit dashboard for creative QA
- ☁️ Connect to Azure Blob or S3 for enterprise delivery
- 🧮 Add prompt templating and metadata tagging
- 🧠 Include semantic brand safety scoring

---

## ❤️ Credits

- **Stability AI** — SDXL v1 API
- **ComfyUI** — Node-based generative workflow inspiration
- **Pillow · PyYAML · Requests** — compositing foundation

---

## 🏁 License

Released under the **MIT License** — free for experimentation and creative exploration.

---

## 🧠 Keywords

`Generative AI` · `Stability AI` · `ComfyUI` · `Creative Automation` · `Stable Diffusion` · `Marketing Tech` · `Brand Intelligence` · `Pillow` · `Python`
