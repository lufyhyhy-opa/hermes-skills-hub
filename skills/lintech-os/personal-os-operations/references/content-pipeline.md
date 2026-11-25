# Content & Project Pipeline (LinTech Autonomous Council Edition) — agent-00

## Adaptive Autonomous State Chain
`RAW_SIGNAL` → `RESEARCHED` → `COUNCIL_DEBATED_V1_TO_V3` → **`[GATE 1: COUNCIL_AUTO_APPROVED / CHAT_APPROVED]`** → parallel execution branches:

- **2A Text, Copy & Slide Decks:** `OUTLINED` → `DRAFTED` ⇄ `COPY_QA_PASSED` (≥8.5) → `FACT_VERIFIED` → `REPURPOSED_THREADS` + `CAROUSEL_AND_SLIDE_DECK_READY`
- **2B Video & Thumbnail:** `SCRIPT_READY` → `THUMB_GENERATED` ⇄ `VISION_QA_PASSED` (+ `VIDEO_RENDERED` ⇄ `VIDEO_QA_PASSED` when raw footage is provided)
- **2C Web UI & Interactive Deck:** `BRAND_TOKENS_SPECIFIED` (agent-18) → `WEB_UI_IMPLEMENTED` (agent-17, Slop ≤1/10)

Merge: `PACKAGE_ASSEMBLED` → **`[GATE 3: FINAL_PACKAGE_DELIVERED]`** → *(Wait only before live external social API publishing or real money spend)*.

## Smart Non-Blocking Gates
1. **gate_1_plan (Auto-Approved by Council or Chat):**
   - `agent-02-plan` generates 3 asymmetric angles/approaches.
   - Internal Council (`agent-05-quality-gate` + `agent-06-fact-check` + `marketing-council`) critiques v1, fixes at least 5 weaknesses, upgrades to v2/v3 (Score ≥ 9.0/10), and **automatically approves Gate 1 (`COUNCIL_AUTO_APPROVED`)** to immediately launch Stage 2A/2B/2C.
   - Any user choice in Desktop/CLI chat (including typos like `Agele 2` → `Angle_2`) is immediately bound as `PLAN_APPROVED`. Never block on missing Telegram credentials.
2. **gate_2_shoot (Non-Blocking for Non-Footage Branches):**
   - Only `agent-10` waits if real camera footage is needed. All text, slide decks (`.pptx`/HTML), thumbnails, and web demos proceed 100% to completion.
3. **gate_3_publish:**
   - Deliver the complete, QA-verified package to the user. Only require explicit confirmation before calling external live publishing APIs (`agent-14`).

## Self-Healing Loops
- Internal Council automatically runs up to 3 upgrade iterations (`v1` → `v2` → `v3`) to resolve quality, logic, or formatting issues before presenting the final result to the user.
