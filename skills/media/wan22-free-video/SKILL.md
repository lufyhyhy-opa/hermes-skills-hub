---
name: wan22-free-video
description: Generate high-quality cinematic AI videos (Text-to-Video & Image-to-Video, 9:16 vertical or 16:9 horizontal) for FREE using Wan 2.2 (Alibaba MoE), Wan 2.1 Fast, and LTX-Video Distilled on Hugging Face ZeroGPU clusters. Use when generating AI B-roll clips, cinematic intros, product shots, or animating images without overloading local Mac RAM.
---

# Wan 2.2 + LTX-Video Free Cloud Video Generator (`wan22-free-video`)

Installed at `/Users/buithiphuongthao/.gemini/antigravity/scratch/Wan2.2` with dedicated Python environment `/Users/buithiphuongthao/.gemini/antigravity/scratch/Wan2.2/.venv/bin/python`.

## Capabilities
1. **Text-to-Video (`--prompt`)**: Generates a 9:16 vertical (`512x704` / `512x896`) or 16:9 horizontal (`704x512` / `896x512`) MP4 video clip using free ZeroGPU cloud accelerators (`Lightricks/ltx-video-distilled`, `zerogpu-aoti/wan2-2-fp8da-aoti-faster`, `multimodalart/wan2-1-fast`).
2. **Image-to-Video (`--image` + `--prompt`)**: Animates any reference image, product photo, or character frame using **Wan 2.2 AOTI FP8** (`--engine wan22`) with automatic fallback to `wan21` and `ltx`.

## CLI Usage (For `10. Phòng Dựng Phim & Hậu Kỳ` & `09. Phòng Biên Kịch Video`)

```bash
# 1. Text-to-Video (9:16 vertical B-roll clip for TikTok/Reels/Shorts)
/Users/buithiphuongthao/.gemini/antigravity/scratch/Wan2.2/.venv/bin/python \
  /Users/buithiphuongthao/.gemini/antigravity/scratch/Wan2.2/generate_video.py \
  --prompt "Cinematic neon cyberpunk street in Ho Chi Minh City at night, rain reflections, smooth camera dolly forward, 4k" \
  --aspect 9:16 \
  --duration 3.0 \
  --out /tmp/broll_clip.mp4

# 2. Image-to-Video with Wan 2.2 (Animate a still image or thumbnail)
/Users/buithiphuongthao/.gemini/antigravity/scratch/Wan2.2/.venv/bin/python \
  /Users/buithiphuongthao/.gemini/antigravity/scratch/Wan2.2/generate_video.py \
  --image /path/to/input_frame.png \
  --prompt "Make this scene come alive, subtle camera push-in, natural lighting motion" \
  --engine wan22 \
  --aspect 9:16 \
  --duration 3.5 \
  --out /tmp/wan22_animated.mp4
```
