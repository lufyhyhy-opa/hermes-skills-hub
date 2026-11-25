---
name: openmontage
description: "Agentic video production studio (OpenMontage) — end-to-end explainers, cinematic trailers, documentary montages, Remotion & HyperFrames compositions, and reference-video cloning."
version: 1.0.0
author: OpenMontageInc (integrated for Hermes Agent)
license: AGPLv3
platforms: [linux, macos, windows]
metadata:
  tags: [video, openmontage, remotion, hyperframes, documentary, explainer, trailer, piper-tts, ffmpeg]
  hermes:
    tags: [OpenMontage, Video, Remotion, HyperFrames, Explainer, Trailer, Media]
    related_skills: [ai-video-editor, video-rendering-engine, remotion-video-creation]
---

# OpenMontage — Agentic Video Production System for Hermes

OpenMontage is installed and pre-configured at:
`/Users/buithiphuongthao/.gemini/antigravity/scratch/OpenMontage`

With virtual environment:
`/Users/buithiphuongthao/.gemini/antigravity/scratch/OpenMontage/.venv/bin/python`

## When to Use
Use this skill whenever the user wants to:
- Produce a full video from a prompt (animated explainer, documentary montage from real archival/stock footage, cinematic trailer, product launch reel, character animation, or short drama).
- Clone the pacing, hook, and structure of a reference YouTube Short / Reel / TikTok / local video into a new video.
- Render data-driven React compositions (`Remotion`) or HTML/CSS/GSAP motion graphics (`HyperFrames`).
- Open the **Backlot Living Storyboard** (`python -m backlot open`) to monitor and approve stages, scripts, and storyboards live.

## Mandatory Operating Rules (Rule Zero)
1. **Read the Core Contract First:**
   - `/Users/buithiphuongthao/.gemini/antigravity/scratch/OpenMontage/AGENT_GUIDE.md`
   - `/Users/buithiphuongthao/.gemini/antigravity/scratch/OpenMontage/PROJECT_CONTEXT.md`
   - `/Users/buithiphuongthao/.gemini/antigravity/scratch/OpenMontage/.agents/skills/hyperframes-core/references/subagent-dispatch.md`

2. **Run Preflight & Capability Discovery:**
   ```bash
   export PATH="/Users/buithiphuongthao/.hermes/bin:/Users/buithiphuongthao/.hermes/tools/ffmpeg-9.0.1-darwin-arm64:/Users/buithiphuongthao/.hermes/node/bin:/Users/buithiphuongthao/.local/bin:$PATH"
   cd /Users/buithiphuongthao/.gemini/antigravity/scratch/OpenMontage
   ./.venv/bin/python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.provider_menu(), indent=2))"
   ```

3. **Pipeline-First Execution:**
   - Select a pipeline from `/Users/buithiphuongthao/.gemini/antigravity/scratch/OpenMontage/pipeline_defs/<pipeline>.yaml`.
   - Read `/Users/buithiphuongthao/.gemini/antigravity/scratch/OpenMontage/skills/pipelines/<pipeline>/<stage>-director.md` BEFORE executing each stage.
   - Read Layer 3 tool skills in `/Users/buithiphuongthao/.gemini/antigravity/scratch/OpenMontage/.agents/skills/<skill>/SKILL.md` before invoking tools.
