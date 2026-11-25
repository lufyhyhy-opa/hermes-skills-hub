---
name: openui
description: Generate, prototype, and convert live UI components and full web pages (HTML/Tailwind/React/Svelte) from text prompts or reference screenshots using W&B OpenUI (installed locally at /Users/buithiphuongthao/.gemini/antigravity/scratch/openui and running on http://127.0.0.1:7878). Use when designing websites, landing pages, dashboards, UI components, or converting screenshots to code.
---

# OpenUI (`wandb/openui`) — Live UI Prototyping & Screenshot-to-Code Engine

OpenUI is installed locally at `/Users/buithiphuongthao/.gemini/antigravity/scratch/openui` and runs a live web studio on **`http://127.0.0.1:7878`**, pre-connected to:
- **9router Multimodal Models** (`gpt-4o` -> `ag/gemini-4-argon`, `gpt-4o-mini` -> `ag/gemini-3.8-flash-high`, `gpt-4-turbo` -> `ag/claude-sonnet-4-6`, `gpt-3.5-turbo` -> `xai/grok-4.5`)
- **Our Free Model Gateway** (`http://127.0.0.1:18900/v1` — 27 free models under the `LiteLLM` section, including `deepseek-v4.1-flash-free`, `glm-5.3-flash-free`, `nemotron-3.5-super-vl-free`, `kilo-auto/free`)
- **XingChi API (`gpt-6.1-sol`)** via the CLI generator script.

## 1. Generating UI Directly from the Terminal (For `agent-17-web-designer` & `agent-18-brand-designer`)

Use the headless CLI generator `/Users/buithiphuongthao/.gemini/antigravity/scratch/openui/generate_ui.py` to generate complete, self-contained HTML5/Tailwind/JS or React files from a prompt or screenshot:

```bash
# Generate a complete UI / Landing Page from a prompt (uses gpt-6.1-sol by default)
python3 /Users/buithiphuongthao/.gemini/antigravity/scratch/openui/generate_ui.py \
  --prompt "Thiết kế Landing Page SaaS AI hiện đại, Dark Mode, Bento Grid 7/5, font Be Vietnam Pro" \
  --out /tmp/landing_preview.html

# Convert a reference screenshot into clean HTML + Tailwind CSS code (uses Vision model)
python3 /Users/buithiphuongthao/.gemini/antigravity/scratch/openui/generate_ui.py \
  --prompt "Clone giao diện trong ảnh này sang HTML5 + Tailwind CSS chuẩn responsive, hỗ trợ tiếng Việt" \
  --image /path/to/screenshot.png \
  --out /tmp/cloned_ui.html
```

## 2. Managing the Live OpenUI Web Studio (`http://127.0.0.1:7878`)

- **Check if OpenUI Studio is running**:
  ```bash
  curl -sS http://127.0.0.1:7878/v1/models
  ```
- **Start / Restart OpenUI Studio in background**:
  ```bash
  cd /Users/buithiphuongthao/.gemini/antigravity/scratch/openui/backend && \
  nohup .venv/bin/python -m openui >/tmp/openui-server.log 2>&1 &
  ```
