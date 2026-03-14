# 🎨 ComfyUI Production Pipeline

**Author:** [Jules Gerard](https://github.com/discofuchsia) — AI Video Engineer & Creative Technologist

> "Node-based visual AI workflows — from prompt to production."

---

## 🚀 Overview

A **production-grade generative AI pipeline** built on **ComfyUI**, **Stable Diffusion XL**, and **Python**. This system powers automated visual content generation at enterprise scale — from text-to-image, image-to-image, to image-to-video workflows.

Built from real-world experience generating visual content for 7,000+ brands at scale.

### What This Does

- **Text-to-Image**: SDXL generation with ControlNet composition control
- **Image-to-Image**: Style transfer, brand consistency, img2img refinement
- **Image-to-Video**: Wan2.2 (81 frames from a single image) via ComfyUI Cloud
- **LoRA Fine-tuning**: Custom model adaptation for brand-specific styles
- **Quality Pipeline**: Automated brand compliance, QA reporting, batch processing

---

## 🔧 ComfyUI Workflows

### Text-to-Image (SDXL + ControlNet)
```
Load Checkpoint → CLIP Encode (prompt) → KSampler → VAE Decode → Save Image
                                      ↑
                        ControlNet (Canny/Depth/Pose)
```
- ControlNet types: Canny (edges), Depth (composition), OpenPose (characters)
- CFG scale 7-8, cosine noise schedule, 25 steps

### Image-to-Image (Style Transfer)
```
Load Image → VAE Encode → KSampler (denoise 0.4-0.6) → VAE Decode → Save
                        ↑
              ControlNet (maintain structure)
```
- Lower denoise = more faithful to source, higher = more creative

### Image-to-Video (Wan2.2)
```
Load Image → Wan2.2 Model → 81 Frames → Frame Interpolation → Video Encode
```
- Temporal consistency via cross-frame attention
- Output: MP4, configurable FPS and duration

### LoRA Integration
```
Load Checkpoint → Load LoRA (weight 0.6-1.0) → CLIP Encode → KSampler → Output
```
- Training: 20-50 images, 1000-3000 steps, rank 4-32, lr 1e-4

### Upscaling
```
Load Image → ESRGAN 4x → Tile Upscale → Color Correct → Sharpen → Save
```

---

## 📁 Project Structure

```
stable_diffusion/
├── app.py                          # CLI orchestrator
├── briefs/sample_brief.yaml        # Campaign brief template
├── pipeline/
│   ├── generators.py               # Provider routing & fallback logic
│   ├── adapters.py                 # Dimension snapping & resizing
│   ├── providers/
│   │   ├── comfyui_api.py          # ComfyUI Cloud API integration
│   │   ├── stability_api.py        # Stability AI SDXL API
│   │   └── sdxl_diffusers.py       # Local HuggingFace Diffusers
│   ├── layout.py                   # Brand overlay compositing
│   ├── brand_checks.py             # Palette & compliance validation
│   └── reporting.py                # CSV QA report generation
├── train_diffusion.py              # Train DDPM from scratch
├── requirements.txt
└── README.md
```

---

## ⚡ Quickstart

```bash
git clone https://github.com/discofuchsia/stable_diffusion.git
cd stable_diffusion
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Generate from brief
python app.py briefs/sample_brief.yaml

# Train diffusion model from scratch
python train_diffusion.py --dataset mnist --epochs 50 --cfg
```

---

## 🧪 Diffusion Training (from scratch)

`train_diffusion.py` implements a complete DDPM with:
- **Forward process**: Gaussian noise addition with cosine schedule
- **U-Net**: Encoder/bottleneck/decoder with time embeddings and skip connections
- **Loss**: MSE on noise prediction
- **Sampling**: Full DDPM (1000 steps)
- **Classifier-free guidance**: 10% unconditional dropout, guided inference
- **Datasets**: MNIST, CIFAR-10

---

## 🎬 Portfolio

- **AI Video Reel:** [youtu.be/IPY8PrRrpGc](https://youtu.be/IPY8PrRrpGc)
- **DreamWorks Animation:** 7 major features including Puss in Boots, Trolls, How to Train Your Dragon

---

## 🛠️ Built With

**Generation:** Stable Diffusion XL · ComfyUI · ControlNet · Wan2.2 · ESRGAN
**ML:** PyTorch · LoRA · Diffusers · sentence-transformers
**Infrastructure:** Python · Docker · Azure · AWS · REST APIs

---

**Keywords:** ComfyUI · Stable Diffusion · ControlNet · Wan2.2 · LoRA · Diffusion Models · Creative Automation · Python · PyTorch
