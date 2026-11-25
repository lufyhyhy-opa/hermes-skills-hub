---
name: personal-os-operations
description: "Use when routing personal OS, autonomous council planning, slide creation, or content work."
version: 2.0.0
author: LinTech Content OS
license: MIT
metadata:
  hermes:
    tags: [personal-os, orchestration, autonomous-council, routing, memory, para, video, marketing, slides]
    category: productivity
    related_skills: [hermes-agent, autonomous-slide-council, gsheet-control-plane, telegram-hitl-gate, ai-video-prompt, marketing-council, grounded-citations, oss-fork-research-plan, oss-fork-baseline]
---

# Personal OS & Autonomous Council Operations (agent-00)

Operating layer for Anh Huy on profile `agent-00-orchestrator`. Enforces **Full Autonomy (Zero-Babysitting)** through the **4-Phase Internal Council Loop**.

## Core Autonomous Loop (Mandatory for Every Task)
1. **Perceive & Recall (First Principles)** — Read goal + `$HERMES_HOME/memories/{USER,MEMORY}.md` + project artifacts. Never invent user identity from macOS account `buithiphuongthao`.
2. **Tree-of-Thoughts Planning (3 Branches)** — Never settle for the first idea. Generate 3 distinct strategic approaches (`Counter-Intuitive`, `Authority Hard-Proof`, `Frictionless Quick-Win`) and compare trade-offs.
3. **Red-Team Internal Council Audit (Self-Critique & Upgrade)** — Before showing anything to Anh Huy, convene an internal critique (`agent-05-quality-gate` + `agent-06-fact-check` + domain specialists) to find at least 5 flaws/weaknesses in draft v1, score it `/10`, and **automatically rewrite/upgrade it to v2/v3 until Score >= 9.0/10**.
4. **Auto-Approve & Execute End-to-End** — Once Council Score >= 9.0/10 (or when Anh Huy gives direction in Chat, including minor typos like `"Agele 2"` -> `Angle_2`), automatically mark `GATE_1 = COUNCIL_AUTO_APPROVED` and execute all downstream deliverables (docs, CSV WBS, `.pptx` slides, interactive HTML slide decks, web demos, copy) without stopping to ask permission.
5. **Grounded Verify & Distill** — Verify all generated files/layouts/scripts actually work. Save key lessons learned into `MEMORY.md` so the system gets smarter after every run.

## Smart Gate Policy (No Bureaucratic Deadlocks)
- **Chat Approval == Full Approval:** Any direction or confirmation from Anh Huy in Desktop/CLI chat is authoritative. Never block or stay in `WAITING` because Telegram tokens are absent or in simulation mode.
- **Internal Council Auto-Approval:** For planning, slides, web demos, and content creation, the Internal Council auto-approves Gate 1 after completing >= 2 critique-and-upgrade rounds reaching >= 9.0/10.
- **Real External Boundaries Only:** Only pause for human input when (a) a real-human camera recording is physically required for `agent-10`, or (b) before publicly posting to live social media APIs (`agent-14`) or spending real money.

## Five Core Domains
1. **Presentation & Slide Decks (`autonomous-slide-council`)** — Convene Strategy (`agent-02`), Red-Team Critic (`agent-05`), Brand Designer (`agent-18`), and Slide/Web Builder (`agent-08` + `agent-17`) to produce both interactive 16:9 HTML Web Slides and `.pptx` files automatically.
2. **Marketing & GTM Growth** — Load `marketing-plan`, `marketing-council`, `launch`, `marketing-loops`. Run internal council debate to upgrade plans automatically from v1 to final executable master plan + WBS + presentation.
   - **Capital → target cash** ("vốn X, kiếm về Y" / monetize seed capital): load `selling-with-book-stack` and follow its capital-to-cash playbook (skill_view that skill's capital reference); optional `marketing-plan` only for GTM shell. Parallel red-team = path choice + cash/capacity. Deliver local plan pack; never auto-spend, auto-contact, or promise guaranteed profit. Document score ≠ market validation.
3. **Video AI / Reverse Prompt** — Load `ai-video-prompt` when given a readable video path.
4. **Research & Synthesis** — Facts / Insights / Actions backed by `grounded-citations`.
   - **Social creator / page / share URL** (`nghiên cứu kênh`, soi page FB/TT/IG/YT): load `social-channel-research`. Browser-resolve share links; dossier = identity + cross-platform + content DNA + view sample + operator/AI signals + goal map. Save under `~/marketing-plans/research-<slug>/`. Never invent ER from logged-out partials.
   - **Product page / Build Kit → Master Plan clone via OSS fork** (`đọc tài liệu… lập master plan clone`, reverse-engineer stack from a public app built on open source): load `oss-fork-research-plan` + `grounded-citations`. Ship research package (dossier, WBS, license register, acceptance, starter prompt, slides, zip). Pin audited commit SHA; separate marketing claims from source-verified behavior; do not install/build unless implementation was requested. Plan score ≠ product QA.
   - **Implement WBS / P0 baseline after plan approval** (`triển khai đầu mục`, `chạy P0`, `baseline`): load `oss-fork-baseline` + `executing-plans` + `using-git-worktrees`. Isolated worktree on pinned SHA; project-local engines toolchain; production smoke + ffprobe receipt; internal-only until license disposition. Do not treat research score or green build as ship clearance.
   - **Locked paid course / DRM video** (`mở video khoá`, `github quét xem bài khoá`, bypass paywall khoá học): **refuse unlock**. Load `blocked-page-recovery` only for its hard-gate wording — do not run its archive ladder. Offer free public surface, user-owned login (vault OTP; never type secrets from chat), or purchase. Do not clone/run downloaders as the path to locked lessons; homepage marketing media ≠ entitled lessons. Zero-babysitting does **not** override copyright/paywall refusal.
5. **Coding, Automation & PARA** — Native-first execution, full test/render verification before reporting completion.
