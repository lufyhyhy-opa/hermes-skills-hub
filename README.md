# Hermes Skills Hub (`lufyhyhy-opa`)

Kho lưu trữ tổng hợp toàn bộ **Skills**, **Custom Tools/Scripts**, và danh mục các **GitHub Repositories** đã xây dựng & tích hợp trong hệ thống Hermes (`~/.hermes`).

## Tổng quan
- **Tổng số Skills (đã lọc trùng & bỏ 41 skill mặc định):** `196` skills thuộc `18` nhóm
- **Custom Trading Tools:** `tools/ai-trading/` (`crypto_radar.py`, `risk_guard.py`, `trade_journal.py`)
- **Custom Hermes Scripts:** `scripts/` (`hermes-long-horizon-harness`, `hermes-verify-harness`, `sync-hermes-brain.sh`)
- **GitHub Repositories đã tích hợp:** `15` repos
- **Bảo mật:** Đã loại bỏ toàn bộ `.env`, API keys, tokens, database và file tạm trước khi đẩy lên.

## Cấu trúc thư mục
```text
hermes-skills-hub/
├── skills/              # 196 skills phân theo danh mục
├── tools/ai-trading/    # Custom Python CLI tools cho trading
├── scripts/             # Harness & brain sync scripts
├── skills-manifest.json # Metadata JSON của toàn bộ skills
└── README.md
```

## 1. Danh mục GitHub Repositories đã tích hợp trong Hermes

| Repository | Đường dẫn trong `~/.hermes` | Mô tả |
|---|---|---|
| [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) | `hermes-agent` | Core Hermes Agent framework |
| [freqtrade/freqtrade](https://github.com/freqtrade/freqtrade) | `freqtrade` | Open-source crypto trading bot |
| [HKUDS/Vibe-Trading](https://github.com/HKUDS/Vibe-Trading) | `hkuds-vibe-trading` | AI Vibe Trading framework & MCP |
| [VibeTradingLabs/vibetrading](https://github.com/VibeTradingLabs/vibetrading) | `vibetrading` | VibeTrading toolkit |
| [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents) | `tradingagents` | Multi-agent LLM financial trading framework |
| [klinecharts/KLineChart](https://github.com/klinecharts/KLineChart) | `klinechart` | Financial candlestick / K-line charting library |
| [anthropics/skills](https://github.com/anthropics/skills) | `installs/claude-agentic-repos/skills` | Official Anthropic agent skills collection |
| [anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) | `installs/claude-agentic-repos/claude-agent-sdk-python` | Claude Agent SDK (Python) |
| [anthropics/claude-agent-sdk-typescript](https://github.com/anthropics/claude-agent-sdk-typescript) | `installs/claude-agentic-repos/claude-agent-sdk-typescript` | Claude Agent SDK (TypeScript) |
| [anthropics/claude-code-action](https://github.com/anthropics/claude-code-action) | `installs/claude-agentic-repos/claude-code-action` | Claude Code GitHub Action |
| [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | `installs/claude-agentic-repos/awesome-claude-code` | Curated Claude Code skills, hooks & workflows |
| [soyelmismo/hermes-antigravity-subscription](https://github.com/soyelmismo/hermes-antigravity-subscription) | `plugins/antigravity-subscription-directsdk` | Hermes plugin for Antigravity DirectSDK |
| [teknium1/hermes-pixel-office](https://github.com/teknium1/hermes-pixel-office) | `plugins/pixel-office` | Hermes Pixel Office desktop plugin |
| [mintisan/GhostTrackWeb](https://github.com/mintisan/GhostTrackWeb) | `ghosttrack-web` | OSINT tracking web interface |
| [LingyiChen-AI/comfyui-workflow-skill](https://github.com/LingyiChen-AI/comfyui-workflow-skill) | `skills/media/comfyui-workflow-skill` | ComfyUI workflow generation skill |

## 2. Custom Tools & Scripts

### Trading Tools (`tools/ai-trading/`)
- [`crypto_radar.py`](tools/ai-trading/crypto_radar.py) — Quét tín hiệu & thị trường crypto
- [`risk_guard.py`](tools/ai-trading/risk_guard.py) — Kiểm soát rủi ro giao dịch
- [`trade_journal.py`](tools/ai-trading/trade_journal.py) — Nhật ký giao dịch tự động

### Hermes Harness & Sync Scripts (`scripts/`)
- [`hermes-long-horizon-harness`](scripts/hermes-long-horizon-harness)
- [`hermes-verify-harness`](scripts/hermes-verify-harness)
- [`sync-hermes-brain.sh`](scripts/sync-hermes-brain.sh)

## 3. Danh mục toàn bộ Skills theo nhóm

### `ai-engineering` (19)

| Skill | Mô tả |
|---|---|
| [`blueprint-figure`](skills/ai-engineering/blueprint-figure/SKILL.md) | > |
| [`build-project`](skills/ai-engineering/build-project/SKILL.md) | > |
| [`check-understanding`](skills/ai-engineering/check-understanding/SKILL.md) | Phase quiz for AI Engineering from Scratch. Trigger with "quiz me", "test phase", "check my understanding", "do I know phase 3", or `/check-understanding <phase>`. |
| [`claude-certification`](skills/ai-engineering/claude-certification/SKILL.md) | > |
| [`course-guide`](skills/ai-engineering/course-guide/SKILL.md) | > |
| [`course-style`](skills/ai-engineering/course-style/SKILL.md) | > |
| [`find-your-level`](skills/ai-engineering/find-your-level/SKILL.md) | > |
| [`hy-memory`](skills/ai-engineering/hy-memory/SKILL.md) | Dual-system (System 1 + System 2) 8-layer cognitive long-term memory for Hermes Agent powered by Tencent-Hunyuan/Hy-Memory and HyAtlas-Memory (hyatlas-go). Provides Chat Memory (8 |
| [`interview-prep`](skills/ai-engineering/interview-prep/SKILL.md) | > |
| [`isometric-explainer`](skills/ai-engineering/isometric-explainer/SKILL.md) | > |
| [`learn`](skills/ai-engineering/learn/SKILL.md) | > |
| [`learn-agent-skills`](skills/ai-engineering/learn-agent-skills/SKILL.md) | > |
| [`learn-mcp`](skills/ai-engineering/learn-mcp/SKILL.md) | > |
| [`learn-reverse-engineering`](skills/ai-engineering/learn-reverse-engineering/SKILL.md) | > |
| [`lesson-screen`](skills/ai-engineering/lesson-screen/SKILL.md) | > |
| [`mcpa-certification`](skills/ai-engineering/mcpa-certification/SKILL.md) | > |
| [`motion-figure`](skills/ai-engineering/motion-figure/SKILL.md) | > |
| [`start-learning`](skills/ai-engineering/start-learning/SKILL.md) | > |
| [`write-manual`](skills/ai-engineering/write-manual/SKILL.md) | > |

### `anthropics` (19)

| Skill | Mô tả |
|---|---|
| [`academy-guide`](skills/anthropics/academy-guide/SKILL.md) | > |
| [`algorithmic-art`](skills/anthropics/algorithmic-art/SKILL.md) | Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Use this when users request creating art using code, generative art, algorithmic |
| [`brand-guidelines`](skills/anthropics/brand-guidelines/SKILL.md) | Applies Anthropic's official brand colors and typography to any sort of artifact that may benefit from having Anthropic's look-and-feel. Use it when brand colors or style guideline |
| [`canvas-design`](skills/anthropics/canvas-design/SKILL.md) | Create beautiful visual art in .png and .pdf documents using design philosophy. You should use this skill when the user asks to create a poster, piece of art, design, or other stat |
| [`claude-api`](skills/anthropics/claude-api/SKILL.md) | \|- |
| [`discernment-nudge`](skills/anthropics/discernment-nudge/SKILL.md) | > |
| [`doc-coauthoring`](skills/anthropics/doc-coauthoring/SKILL.md) | Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs, decision docs, or similar structur |
| [`docx`](skills/anthropics/docx/SKILL.md) | Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files) or Word templates (.dotx files). Triggers include: any mention of 'Word doc |
| [`frontend-design`](skills/anthropics/frontend-design/SKILL.md) | Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one. Helps with aesthetic direction, typography, and making choices that don't rea |
| [`internal-comms`](skills/anthropics/internal-comms/SKILL.md) | A set of resources to help me write all kinds of internal communications, using the formats that my company likes to use. Claude should use this skill whenever asked to write some |
| [`mcp-builder`](skills/anthropics/mcp-builder/SKILL.md) | Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers |
| [`pdf`](skills/anthropics/pdf/SKILL.md) | Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into one, splitt |
| [`pptx`](skills/anthropics/pptx/SKILL.md) | Use this skill any time a .pptx or .potx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsi |
| [`skill-creator`](skills/anthropics/skill-creator/SKILL.md) | Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run e |
| [`slack-gif-creator`](skills/anthropics/slack-gif-creator/SKILL.md) | Knowledge and utilities for creating animated GIFs optimized for Slack. Provides constraints, validation tools, and animation concepts. Use when users request animated GIFs for Sla |
| [`theme-factory`](skills/anthropics/theme-factory/SKILL.md) | Toolkit for styling artifacts with a theme. These artifacts can be slides, docs, reportings, HTML landing pages, etc. There are 10 pre-set themes with colors/fonts that you can app |
| [`web-artifacts-builder`](skills/anthropics/web-artifacts-builder/SKILL.md) | Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tailwind CSS, shadcn/ui). Use for complex artifacts r |
| [`webapp-testing`](skills/anthropics/webapp-testing/SKILL.md) | Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, a |
| [`xlsx`](skills/anthropics/xlsx/SKILL.md) | Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .xltx, .c |

### `caveman` (10)

| Skill | Mô tả |
|---|---|
| [`caveman-commit`](skills/caveman/caveman-commit/SKILL.md) | Ultra-compressed commit message generator. Cuts noise from commit messages while preserving intent and reasoning. Conventional Commits format. Subject ≤50 chars, body only when \"w |
| [`caveman-compress`](skills/caveman/caveman-compress/SKILL.md) | Compress natural language memory files (CLAUDE.md, todos, preferences) into caveman format to save input tokens. Preserves all technical substance, code, URLs, and structure. Compr |
| [`caveman-evidence-review`](skills/caveman/caveman-evidence-review/SKILL.md) | Review Caveman Cloud evidence read-only: costs, Cave Score, Cave Plan, workflows, traces, latency, errors, compression, routing, and verified savings. Use when the user asks what C |
| [`caveman-review`](skills/caveman/caveman-review/SKILL.md) | Ultra-compressed code review comments. Cuts noise from PR feedback while preserving the actionable signal. Each comment is one line: location, problem, fix. Use when user says \"re |
| [`caveman-stats`](skills/caveman/caveman-stats/SKILL.md) | Show real token usage and estimated savings for the current session. Reads directly from the Claude Code session log — no AI estimation. Triggers on /caveman-stats. Output is injec |
| [`investigate-first`](skills/caveman/investigate-first/SKILL.md) | Diagnose ambiguous failures before editing. Use for unknown causes, intermittent behavior, performance regressions, or investigations needing evidence-ranked hypotheses. |
| [`lean-build`](skills/caveman/lean-build/SKILL.md) | Build feature work with high overbuilding risk. Use for new behavior, product slices, or integrations where repository reuse, strict scope, and an explicit stop condition matter. |
| [`safe-refactor`](skills/caveman/safe-refactor/SKILL.md) | Restructure code while preserving behavior. Use for extraction, consolidation, ownership moves, or cleanup where verification must bracket structural edits. |
| [`surgical-patch`](skills/caveman/surgical-patch/SKILL.md) | Fix bugs and small behavior changes at the narrowest responsible layer. Use when regression proof, preserved surrounding behavior, and task-relevant tests matter. |
| [`verify-and-stop`](skills/caveman/verify-and-stop/SKILL.md) | Prove existing work meets acceptance conditions without expanding scope. Use for validation-only tasks, completion checks, focused gate runs, and last-mile proof. |

### `creative` (2)

| Skill | Mô tả |
|---|---|
| [`opa-content-workspace-design`](skills/creative/opa-content-workspace-design/SKILL.md) | Use when designing OPA plan or content workspace websites. |
| [`openui`](skills/creative/openui/SKILL.md) | Generate, prototype, and convert live UI components and full web pages (HTML/Tailwind/React/Svelte) from text prompts or reference screenshots using W&B OpenUI (installed locally a |

### `crypto-quant` (19)

| Skill | Mô tả |
|---|---|
| [`alpha-zoo`](skills/crypto-quant/alpha-zoo/SKILL.md) | Browse and bench the bundled alpha zoos — prebuilt cross-sectional factor libraries (Kakushadze 101, GTJA 191, Qlib 158, Fama-French / Carhart). Use when the user asks "which alpha |
| [`candlestick`](skills/crypto-quant/candlestick/SKILL.md) | Candlestick pattern recognition engine, pure pandas vectorized implementation of 15 classic candlestick patterns (5 single-candle + 5 double-candle + 4 triple-candle + 1 trend conf |
| [`ccxt`](skills/crypto-quant/ccxt/SKILL.md) | CCXT unified crypto exchange library (100+ exchanges). Free public market data. Fallback when OKX is unavailable. |
| [`chanlun`](skills/crypto-quant/chanlun/SKILL.md) | 基于缠论（缠中说禅）的形态识别引擎，使用czsc库自动检测K线分型、笔、中枢，并生成一买/一卖/二买/二卖/三买/三卖等买卖点信号。支持多周期分析和形态分类（3/5/7/9/11笔形态）。 |
| [`crypto-derivatives`](skills/crypto-quant/crypto-derivatives/SKILL.md) | Crypto-derivatives strategies — perpetual funding-rate arbitrage, futures term-structure contango/backwardation trading, and option volatility-smile / Greeks analysis. |
| [`crypto-hold-research`](skills/crypto-quant/crypto-hold-research/SKILL.md) | Use when screening or capital-planning long-hold coins. |
| [`cycle-money-flow`](skills/crypto-quant/cycle-money-flow/SKILL.md) | Use when forecasting regime, money-flow, or bubble phase. |
| [`defi-yield`](skills/crypto-quant/defi-yield/SKILL.md) | DeFi yield analysis and optimization — lending rates, LP yields, staking returns, yield farming strategies, risk-adjusted yield comparison, and protocol-level sustainability assess |
| [`elliott-wave`](skills/crypto-quant/elliott-wave/SKILL.md) | Elliott Wave Theory signal engine. Detects swing points through Zigzag, matches 5-wave impulse and 3-wave corrective structures, validates them with Fibonacci wave relationships, a |
| [`harmonic`](skills/crypto-quant/harmonic/SKILL.md) | Harmonic Patterns signal engine. Identifies XABCD five-point structures such as Gartley/Bat/Butterfly/Crab based on Fibonacci geometry, and generates trading signals in the PRZ (Po |
| [`ichimoku`](skills/crypto-quant/ichimoku/SKILL.md) | Ichimoku Kinko Hyo five-line system signal engine. A standalone Japanese technical-analysis school that generates trading signals from Tenkan/Kijun crossovers, cloud position, and |
| [`liquidation-heatmap`](skills/crypto-quant/liquidation-heatmap/SKILL.md) | Liquidation level analysis and heatmap interpretation — identify leveraged position concentration, liquidation cascades, stop-hunt zones, and use liquidation data as support/resist |
| [`okx-market`](skills/crypto-quant/okx-market/SKILL.md) | OKX cryptocurrency market data interface. Uses the OKX V5 REST API to retrieve spot, derivatives, index, and other crypto market data, including real-time prices, candlesticks, fun |
| [`onchain-analysis`](skills/crypto-quant/onchain-analysis/SKILL.md) | On-chain data analysis — active addresses / whale tracking / TVL / DEX liquidity, interpretation and signal generation using on-chain valuation metrics such as MVRV / NVT / SOPR. |
| [`perp-funding-basis`](skills/crypto-quant/perp-funding-basis/SKILL.md) | Perpetual futures funding rate analysis and cash-carry basis trading — funding rate regimes, annualized basis signals, carry trade construction, and funding rate arbitrage between |
| [`pine-script`](skills/crypto-quant/pine-script/SKILL.md) | Export backtest strategies to indicator/strategy code for major trading platforms — TradingView, 通达信, 同花顺, 东方财富, MT5. |
| [`smc`](skills/crypto-quant/smc/SKILL.md) | Smart Money Concepts (ICT) signal engine. Uses the smartmoneyconcepts library to implement institutional-trading-school analysis of BOS, ChoCH, FVG, and order blocks (OB). |
| [`token-unlock-treasury`](skills/crypto-quant/token-unlock-treasury/SKILL.md) | Token unlock schedule analysis and project treasury tracking — vesting cliffs, linear unlocks, team/investor/ecosystem token releases, treasury diversification, and sell pressure f |
| [`volatility`](skills/crypto-quant/volatility/SKILL.md) | Volatility strategy. Trades mean reversion based on percentile ranking of historical volatility (HV). Suitable for any OHLCV data. |

### `general` (12)

| Skill | Mô tả |
|---|---|
| [`content-engine`](skills/general/content-engine/SKILL.md) | Create platform-native content systems for X, LinkedIn, TikTok, YouTube, newsletters, and repurposed multi-platform campaigns. Use when the user wants social posts, threads, script |
| [`opa-content-os`](skills/general/opa-content-os/SKILL.md) | Hệ thống 16 AI Agent tự động hóa sản xuất nội dung đa kênh chuẩn LinTech Content OS tích hợp tiêu chuẩn OPA. |
| [`opa-judge`](skills/general/opa-judge/SKILL.md) | Use khi Phase 4 REVIEW cần second opinion từ model khác để giảm self-review bias. Triggers — "second opinion", "cross-model review", "judge review", "adversarial review bằng model |
| [`opa-knowledge`](skills/general/opa-knowledge/SKILL.md) | Use when kiểm tra nguồn OPA. Giữ qualifiers và gates. |
| [`remotion-video-creation`](skills/general/remotion-video-creation/SKILL.md) | Best practices for Remotion - Video creation in React. 29 domain-specific rules covering 3D, animations, audio, captions, charts, transitions, and more. Use when building video in |
| [`script-video-global`](skills/general/script-video-global/SKILL.md) | Short-form video scripts for TikTok, Reels, YouTube Shorts — 2 A/B variants, 6 hook formulas, timestamp breakdown, shoot guide, caption + hashtag, viral score. Reads `.agents/produ |
| [`social-carousel`](skills/general/social-carousel/SKILL.md) | A three-card social-media carousel laid out as 1080×1080 squares — three cinematic, on-brand panels with display headlines that connect across the series (\"onwards.\" → \"to the n |
| [`social-platform-publishing-engine`](skills/general/social-platform-publishing-engine/SKILL.md) | Use when integrating social OAuth or publishing videos. |
| [`social-video-intel`](skills/general/social-video-intel/SKILL.md) | Use when extracting and transcribing social video content. |
| [`video-content-repurposing`](skills/general/video-content-repurposing/SKILL.md) | Use when repurposing video into multi-platform content. |
| [`video-rendering-engine`](skills/general/video-rendering-engine/SKILL.md) | Use when rendering video, burning subtitles, or assembling. |
| [`video-transcription-edit-planning`](skills/general/video-transcription-edit-planning/SKILL.md) | Use when transcribing video or creating AI edit plans. |

### `lintech-os` (19)

| Skill | Mô tả |
|---|---|
| [`ai-video-editor`](skills/lintech-os/ai-video-editor/SKILL.md) | Say 'Edit my video' (and attach a clip) to use this. Edits real footage by conversation or on autopilot: transcribes it, cuts the filler and dead air, FINDS and PLACES B-roll on th |
| [`autonomous-slide-council`](skills/lintech-os/autonomous-slide-council/SKILL.md) | Hội đồng 4 Agent tự động họp, phản biện kịch bản McKinsey SCQA và xuất Slide thuyết trình hoàn chỉnh (.html tương tác 16:9 & .pptx) không cần con người sửa lỗi thủ công. |
| [`claude-agentic-stack-and-harnesses`](skills/lintech-os/claude-agentic-stack-and-harnesses/SKILL.md) | Hệ quy chiếu Kiến Trúc Tác Nhân Tự Trị của Anthropic & Kho 240+ GitHub Claude Code (tổng hợp từ @kevindatas / Anthropic Research: Building Effective Agents, Effective Harnesses for |
| [`ghosttrack-osint`](skills/lintech-os/ghosttrack-osint/SKILL.md) | OSINT & Digital Footprint Reconnaissance Web Dashboard and API (mintisan/GhostTrackWeb). Tracks IP geolocation/ASN/ISP, international phone number carrier/region/timezone, social m |
| [`gsheet-control-plane`](skills/lintech-os/gsheet-control-plane/SKILL.md) | Use when reading or updating the LinTech Content OS Google Sheet Control Plane (Brand_Memory, Content_Pipeline, Performance_KPI) or synchronizing product-marketing context across a |
| [`harness-engineering-trust-pyramid`](skills/lintech-os/harness-engineering-trust-pyramid/SKILL.md) | Hệ quy chiếu Harness Engineering & Kim Tự Tháp Niềm Tin 4 Tầng (Lauren Tan — SpaceX/xAI GrokBot Playbook: 3.000 PR/tháng, 0.5% Rollback). Áp dụng nguyên tắc 'Lint > AGENTS.md', khó |
| [`huy-intent-and-gold-standards`](skills/lintech-os/huy-intent-and-gold-standards/SKILL.md) | Bộ Giải Mã Ý Định Ngầm (Nói 1 Hiểu 10) và Kho Mẫu Chuẩn Vàng 10/10 (Few-Shot Gold Standards) dành riêng cho Anh Huy (Huy × OPA / LinTech OS). Nạp kỹ năng này khi cần hiểu sâu ý địn |
| [`lintech-copy-engine`](skills/lintech-os/lintech-copy-engine/SKILL.md) | Use when outlining, writing, humanizing, scoring (LLM Judge 0-10), or repurposing text posts, Threads, and 6-7 slide Carousels. Integrates coreyhaines31/marketingskills (Seven Swee |
| [`personal-os-operations`](skills/lintech-os/personal-os-operations/SKILL.md) | Use when routing personal OS, autonomous council planning, slide creation, or content work. |
| [`remotion-kinetic-overlays`](skills/lintech-os/remotion-kinetic-overlays/SKILL.md) | Unified Remotion library for Short-Form Kinetic Typography, Word-Level Animated Captions (13 themes including Hormozi/Hustle, MrBeast, Karaoke, Kinetic, Pop), and B-Roll Cutaway Ov |
| [`sfxmint`](skills/lintech-os/sfxmint/SKILL.md) | Add free CC0 sound effects to a web app or game, free to try with no API key, using the SFXMint API (sound roles, sets grouped by event, search) and permanent hotlinkable MP3 and W |
| [`short-video-scripting`](skills/lintech-os/short-video-scripting/SKILL.md) | Use when writing 35-55 second short-form video scripts (TikTok, Reels, YouTube Shorts) with 3-second retention hooks, teleprompter-ready spoken Vietnamese lines, camera shotlists, |
| [`social-ops-analytics`](skills/lintech-os/social-ops-analytics/SKILL.md) | Use when publishing approved content across TikTok, Facebook Reels, YouTube Shorts, Threads, and Telegram with idempotency protection (Agent 14), automating keyword comment-to-DM l |
| [`telegram-hitl-gate`](skills/lintech-os/telegram-hitl-gate/SKILL.md) | Use when dispatching Human-in-the-Loop approval cards to Telegram Bot for Gate 1 (Plan Approval), Gate 2 (Raw Video Shooting Sheet), and Gate 3 (Final Multi-Channel Release Gate). |
| [`thumbnail-vision-audit`](skills/lintech-os/thumbnail-vision-audit/SKILL.md) | Use when designing high-CTR 9:16 and 3:4 video thumbnails (Ideogram 3.0, Flux, Gemini Image) for Agent 12 and executing Multimodal Vision QA checks (Vietnamese OCR typo check, TikT |
| [`trend-radar-scraper`](skills/lintech-os/trend-radar-scraper/SKILL.md) | Use when scanning daily tech/industry trends, extracting native TikTok WebVTT subtitles and comment insights (Zero-Compute), or fact-checking claims and statistics against primary |
| [`video-autocut-pipeline`](skills/lintech-os/video-autocut-pipeline/SKILL.md) | Use when processing raw talking-head video clips into vertical 9:16 short-form videos: 16kHz audio demuxing, Faster-Whisper word-level transcription, VAD silence removal (>0.4s), m |
| [`video-short`](skills/lintech-os/video-short/SKILL.md) | Turn a raw talking-head recording into a finished 1080x1920 Short, Reel, or TikTok with B-roll, motion graphics, captions, and music. Shows the plan in chat, then iterates on draft |
| [`web-ui-ux-pro-max`](skills/lintech-os/web-ui-ux-pro-max/SKILL.md) | Use when designing and implementing production-grade Web UI/UX, High-Conversion Landing Pages, SaaS Dashboards, Design Systems (DESIGN.md tokens), Bento Grids, and Interactive Prot |

### `marketing` (1)

| Skill | Mô tả |
|---|---|
| [`selling-with-book-stack`](skills/marketing/selling-with-book-stack/SKILL.md) | Use when explicitly asked to sell or monetize. |

### `marketingskills` (53)

| Skill | Mô tả |
|---|---|
| [`marketingskills-ab-testing`](skills/marketingskills/marketingskills-ab-testing/SKILL.md) | When the user wants to plan, run, or read A/B tests, or asks a judgement call on one: is the result real, can we stop, which version won, is this worth testing at all: sample size, |
| [`marketingskills-ad-creative`](skills/marketingskills/marketingskills-ad-creative/SKILL.md) | When the user wants to write or judge ad creative, or asks which ad, hook, or angle to run or kill: headlines, primary text, and variations for Google, Meta, LinkedIn, and TikTok, |
| [`marketingskills-ads`](skills/marketingskills/marketingskills-ads/SKILL.md) | When the user wants to plan, run, or fix paid ads on Google, Meta, and LinkedIn, or asks a judgement call on them: are ads worth it, which channel or budget split, why CPA rose, ki |
| [`marketingskills-ai-seo`](skills/marketingskills/marketingskills-ai-seo/SKILL.md) | When the user wants to get cited and recommended in AI answers (ChatGPT, Perplexity, AI Overviews), or asks why AI cites a competitor, which content gets cited, or whether llms.txt |
| [`marketingskills-analytics`](skills/marketingskills/marketingskills-analytics/SKILL.md) | When the user wants to set up or audit analytics, or asks whether a metric or number is calculated right, what to track, or how to name events: tracking plans, GA4, GTM, Mixpanel, |
| [`marketingskills-aso`](skills/marketingskills/marketingskills-aso/SKILL.md) | When the user wants to audit or optimize an App Store or Google Play listing, or asks which title, keywords, or screenshots to pick or why downloads are low: subtitle, description, |
| [`marketingskills-attribution`](skills/marketingskills/marketingskills-attribution/SKILL.md) | When the user wants to work out which marketing drives revenue, or asks whether a channel is really working, which numbers to trust, or how to credit podcasts and dark social: attr |
| [`marketingskills-churn-prevention`](skills/marketingskills/marketingskills-churn-prevention/SKILL.md) | When the user wants to reduce churn, or asks why customers cancel, whether to offer a discount or pause: cancellation flows, exit surveys, save offers, dunning and failed-payment r |
| [`marketingskills-co-marketing`](skills/marketingskills/marketingskills-co-marketing/SKILL.md) | When the user wants co-marketing partners or joint campaigns, or asks whether a partner fits, a size mismatch matters, or how to split work and leads: integration partners, cross-p |
| [`marketingskills-cold-email`](skills/marketingskills/marketingskills-cold-email/SKILL.md) | When the user wants to write or run B2B cold outbound, or asks whether an opener, reason to reach out, or email works or why nobody replies: cold emails, follow-ups, sending domain |
| [`marketingskills-community-marketing`](skills/marketingskills/marketingskills-community-marketing/SKILL.md) | When the user wants to build or grow an online community, or asks whether a community is worth it, where to host it, or why members stay quiet: Discord, Slack, forums, participatio |
| [`marketingskills-competitor-profiling`](skills/marketingskills/marketingskills-competitor-profiling/SKILL.md) | When the user wants to research competitors into dated profiles, or asks what a rival charges, claims, or is doing, or whether a conclusion about them is fair: positioning, pricing |
| [`marketingskills-competitors`](skills/marketingskills/marketingskills-competitors/SKILL.md) | When the user wants to create or audit comparison and alternative pages ('X vs Y', 'X alternative', 'best X alternatives'), or asks what a public page may say about a competitor: p |
| [`marketingskills-content-strategy`](skills/marketingskills/marketingskills-content-strategy/SKILL.md) | When the user wants to plan content, or asks which topic or piece to prioritize, what to write about, or why posts bring no customers: topic clusters, editorial calendars, roadmaps |
| [`marketingskills-conversion-tracking`](skills/marketingskills/marketingskills-conversion-tracking/SKILL.md) | When the user wants to set up, audit, or fix conversion tracking to Google Ads, Meta, GA4, LinkedIn, and TikTok, or asks why conversions are missing or doubled: GTM, pixels, CAPI, |
| [`marketingskills-copy-editing`](skills/marketingskills/marketingskills-copy-editing/SKILL.md) | When the user wants to edit, tighten, proofread, or refresh existing copy, or asks whether to keep, cut, or change a line in it, without rewriting from scratch. Every edit removes |
| [`marketingskills-copywriting`](skills/marketingskills/marketingskills-copywriting/SKILL.md) | When the user wants to write or rewrite page copy (homepage, landing, pricing, feature), or asks which headline, promise, or message to lead with. Diagnoses the input first (blank |
| [`marketingskills-cro`](skills/marketingskills/marketingskills-cro/SKILL.md) | When the user wants more conversions from a page or form, or asks why a page isn't converting, what to change first, or whether to add or remove a field or element: landing and pri |
| [`marketingskills-customer-research`](skills/marketingskills/marketingskills-customer-research/SKILL.md) | When the user wants to run or synthesize customer research, or asks what customer quotes, reviews, or feedback really mean, what is safe to conclude, and what to ask next: intervie |
| [`marketingskills-directory-submissions`](skills/marketingskills/marketingskills-directory-submissions/SKILL.md) | When the user wants to list a product in startup, SaaS, AI, MCP, and review directories, or asks which directories are worth it or whether listings are working: Product Hunt, G2, C |
| [`marketingskills-emails`](skills/marketingskills/marketingskills-emails/SKILL.md) | When the user wants to create or improve automated email sequences, or asks what to send, when, or whether an email or flow is working: welcome, onboarding, nurture, and win-back f |
| [`marketingskills-events`](skills/marketingskills/marketingskills-events/SKILL.md) | When the user wants to plan, run, sponsor, or speak at events, or asks whether an event or booth is worth the money: webinars, conferences, booths, meetups, show-up rates, and foll |
| [`marketingskills-free-tools`](skills/marketingskills/marketingskills-free-tools/SKILL.md) | When the user wants to plan or build a free tool as marketing, or asks whether a tool idea is worth building or which one to pick: calculators, graders, generators, and other inter |
| [`marketingskills-image`](skills/marketingskills/marketingskills-image/SKILL.md) | When the user wants to create, generate, edit, or optimize marketing images, or asks which approach to take (generate, design, or photograph): blog heroes, social graphics, product |
| [`marketingskills-influencer-marketing`](skills/marketingskills/marketingskills-influencer-marketing/SKILL.md) | When the user wants creator, influencer, or ambassador partnerships, or asks which creators fit, what to pay, which rights to buy, or whether a sponsorship worked: vetting, contrac |
| [`marketingskills-launch`](skills/marketingskills/marketingskills-launch/SKILL.md) | When the user wants to plan a product or feature launch, or asks whether it's ready, when to announce, or how to get noticed: Product Hunt, beta and early access, waitlists, releas |
| [`marketingskills-lead-magnets`](skills/marketingskills/marketingskills-lead-magnets/SKILL.md) | When the user wants to plan or improve a lead magnet, or asks what to give away for emails or how much to ask in return (gating, form fields): checklists, templates, ebooks, gated |
| [`marketingskills-link-building`](skills/marketingskills/marketingskills-link-building/SKILL.md) | When the user wants backlinks and mentions that lift rankings and AI citations, or asks how to get sites to link or whether a link tactic is safe: link gaps, unlinked mentions, bro |
| [`marketingskills-marketing-council`](skills/marketingskills/marketingskills-marketing-council/SKILL.md) | When the user wants several expert takes on a marketing decision, or asks what a famous marketer would say about it: a simulated board (Seth Godin, David Ogilvy, April Dunford, Byr |
| [`marketingskills-marketing-ideas`](skills/marketingskills/marketingskills-marketing-ideas/SKILL.md) | When the user wants marketing ideas or growth tactics for a software product, or asks what to try to get attention or the next customers with little time or budget, or after the ob |
| [`marketingskills-marketing-loops`](skills/marketingskills/marketingskills-marketing-loops/SKILL.md) | When the user wants a recurring marketing job an AI agent runs on a cadence or trigger, or asks what a weekly or daily automated check should do, remember, and when it should stop: |
| [`marketingskills-marketing-plan`](skills/marketingskills/marketingskills-marketing-plan/SKILL.md) | When the user wants a full marketing or go-to-market plan for a client, an advised company, or their own product, or asks how to sequence or prioritize several initiatives with a f |
| [`marketingskills-marketing-psychology`](skills/marketingskills/marketingskills-marketing-psychology/SKILL.md) | When the user wants to apply psychology to marketing, or asks why buyers behave or value things as they do, or whether a persuasion tactic is honest: biases, mental models, anchori |
| [`marketingskills-offers`](skills/marketingskills/marketingskills-offers/SKILL.md) | When the user wants to design or improve the offer itself, or asks why it isn't selling or how to add urgency honestly: value stacking, bonuses, guarantees, scarcity, payment plans |
| [`marketingskills-onboarding`](skills/marketingskills/marketingskills-onboarding/SKILL.md) | When the user wants better onboarding and activation, or asks why new users don't stick or what the first session should do: first-run experience, aha moments, checklists, empty st |
| [`marketingskills-paywalls`](skills/marketingskills/marketingskills-paywalls/SKILL.md) | When the user wants to create or improve in-app paywalls and upgrade moments, or asks when or how hard to ask free users to pay (after they've seen value): upgrade screens, upsell |
| [`marketingskills-popups`](skills/marketingskills/marketingskills-popups/SKILL.md) | When the user wants to create or improve popups, modals, slide-ins, sticky bars, and banners, or asks whether one will help or annoy and when to show it: exit intent, email capture |
| [`marketingskills-pricing`](skills/marketingskills/marketingskills-pricing/SKILL.md) | When the user wants to set pricing and packaging, or asks what to charge, whether to raise prices, or how to move existing customers: tiers, value metrics, per-seat vs usage, freem |
| [`marketingskills-product-marketing`](skills/marketingskills/marketingskills-product-marketing/SKILL.md) | When the user wants to create or update the product marketing context doc (.agents/product-marketing.md), or asks what belongs in it or whether positioning or ICP is clear enough: |
| [`marketingskills-programmatic-seo`](skills/marketingskills/marketingskills-programmatic-seo/SKILL.md) | When the user wants SEO pages at scale from templates and data, or asks whether a page set will rank or look thin: location, integration, comparison, directory, and '[X] for [Y]' p |
| [`marketingskills-prospecting`](skills/marketingskills/marketingskills-prospecting/SKILL.md) | When the user wants to find and qualify prospects for outbound, or asks who to target first, which signal to prioritize, or where to spot buyers with the problem: buying signals, e |
| [`marketingskills-public-relations`](skills/marketingskills/marketingskills-public-relations/SKILL.md) | When the user wants press and media coverage, or asks what to say to a reporter, whether a story is newsworthy, or how to handle a crisis: pitches, press releases, media lists, HAR |
| [`marketingskills-referrals`](skills/marketingskills/marketingskills-referrals/SKILL.md) | When the user wants referral and affiliate programs or word of mouth, or asks what to reward, how much to pay, or which loop to start with: refer-a-friend incentives, commissions a |
| [`marketingskills-reverse-engineer-marketing`](skills/marketingskills/marketingskills-reverse-engineer-marketing/SKILL.md) | When the user wants to know how another company grew and what to copy, or asks what a competitor did and when: a dated log of their moves against their traffic from public data, ar |
| [`marketingskills-revops`](skills/marketingskills/marketingskills-revops/SKILL.md) | When the user wants to design revenue operations, or asks when a lead is ready for sales or why sales and marketing disagree on lead quality: lifecycle stages, MQL and SQL, scoring |
| [`marketingskills-sales-enablement`](skills/marketingskills/marketingskills-sales-enablement/SKILL.md) | When the user wants sales collateral, or asks what to give a champion or rep, or how to answer an objection or make the case: decks, one-pagers, objection handling, demo scripts, t |
| [`marketingskills-schema`](skills/marketingskills/marketingskills-schema/SKILL.md) | When the user wants to add, fix, or validate schema markup (JSON-LD), or asks which type fits a page or whether some markup is allowed: product, review, recipe, FAQ, rich result el |
| [`marketingskills-seo-audit`](skills/marketingskills/marketingskills-seo-audit/SKILL.md) | When the user wants to audit or diagnose SEO, or asks why traffic dropped, a page won't rank, or whether a setup like canonicals, hreflang, or redirects is right: technical SEO, in |
| [`marketingskills-signup`](skills/marketingskills/marketingskills-signup/SKILL.md) | When the user wants better signup, registration, and trial start flows, or asks which fields or steps to cut or whether to require a card: SSO and drop-off before an account exists |
| [`marketingskills-site-architecture`](skills/marketingskills/marketingskills-site-architecture/SKILL.md) | When the user wants to plan or restructure a website, or asks which pages they need or where something belongs: hierarchy, navigation, URL structure, internal linking, website buil |
| [`marketingskills-sms`](skills/marketingskills/marketingskills-sms/SKILL.md) | When the user wants SMS, MMS, or WhatsApp marketing, or asks whether texting is worth it or a message is allowed: abandoned cart, win-back, and promo texts, WhatsApp templates and |
| [`marketingskills-social`](skills/marketingskills/marketingskills-social/SKILL.md) | When the user wants organic social content for LinkedIn, X, Instagram, TikTok, or Facebook, or asks what to post, which format to favor, or from which account: posts, threads, caro |
| [`marketingskills-video`](skills/marketingskills/marketingskills-video/SKILL.md) | When the user wants to create video with AI tools or code, or asks which approach to use (screen recording, AI avatar, generated, or templated) or how to make videos repeatably: pr |

### `media` (8)

| Skill | Mô tả |
|---|---|
| [`ai-video-prompt`](skills/media/ai-video-prompt/SKILL.md) | Reverse-engineer any reference video into scene-by-scene (shot-by-shot) generation prompts, character/avatar look specs, camera movements, and evidence frames for HeyGen, Seedance, |
| [`comfyui-family-filmmaker`](skills/media/comfyui-family-filmmaker/SKILL.md) | Sản xuất phim ngắn gia đình 3 nhân vật người thật (Ba, Mẹ, Con gái) theo công thức triệu view của kênh "Linh Mít Daily" (9:16 Reels/TikTok 15-18s) bằng Quy trình 3 bước trên ComfyU |
| [`comfyui-workflow-skill`](skills/media/comfyui-workflow-skill/SKILL.md) | Generate ready-to-use ComfyUI workflow JSON files (txt2img, img2img, txt2vid, img2vid, upscale, inpaint, ControlNet, LoRA, Wan2.2, FLUX, SDXL) through natural language conversation |
| [`hypit`](skills/media/hypit/SKILL.md) | Clone any viral video and direct/produce multi-variant videos with Hypit (hypit-ai/hypit). Word-anchored SVML/SVS/SVRun video workflow language & runtime: swap faces/avatars, scrip |
| [`openmontage`](skills/media/openmontage/SKILL.md) | Agentic video production studio (OpenMontage) — end-to-end explainers, cinematic trailers, documentary montages, Remotion & HyperFrames compositions, and reference-video cloning. |
| [`rea-video`](skills/media/rea-video/SKILL.md) | 逆向拆解一条视频是怎么做出来的——逐镜头判断实拍 / 影视片段 / AI 生成 / 3D 渲染 / 2D 动画 / 定格动画 / 代码模板渲染 / 录屏截图 / 静态图推拉 / 静帧，以及实拍是否经过 AI 加工（换脸、对口型、风格化），标出后期叠加层（逐句字幕时间轴、花字、标题、贴纸 / GIF / 表情包、画中画）和用户真实素材，拆解人声、背景音乐、音效 |
| [`video-shotcraft`](skills/media/video-shotcraft/SKILL.md) | Create cinematic product promo videos and B-roll motion graphics from frontend projects, web pages, or scripts using Remotion, 124+ shot recipe cards (2.5D camera moves, UI entranc |
| [`wan22-free-video`](skills/media/wan22-free-video/SKILL.md) | Generate high-quality cinematic AI videos (Text-to-Video & Image-to-Video, 9:16 vertical or 16:9 horizontal) for FREE using Wan 2.2 (Alibaba MoE), Wan 2.1 Fast, and LTX-Video Disti |

### `planning` (1)

| Skill | Mô tả |
|---|---|
| [`planning-with-files`](skills/planning/planning-with-files/SKILL.md) | Manus-style persistent file-based planning for AI coding agents: keeps task_plan.md, findings.md, and progress.md on disk so work survives context loss and /clear. Use when asked t |

### `ponytail` (5)

| Skill | Mô tả |
|---|---|
| [`ponytail-audit`](skills/ponytail/ponytail-audit/SKILL.md) | Whole-repo audit for over-engineering. Like ponytail-review, but scans the entire codebase instead of a diff: a ranked list of what to delete, simplify, or replace with stdlib/nati |
| [`ponytail-debt`](skills/ponytail/ponytail-debt/SKILL.md) | Harvest every `ponytail:` comment in the codebase into a debt ledger, so the deliberate shortcuts and deferrals ponytail leaves behind get tracked instead of rotting into \"later m |
| [`ponytail-gain`](skills/ponytail/ponytail-gain/SKILL.md) | Show ponytail's measured impact as a compact scoreboard: less code, less cost, more speed, from the benchmark medians. One-shot display, not a persistent mode, and not a per-repo n |
| [`ponytail-help`](skills/ponytail/ponytail-help/SKILL.md) | Quick-reference card for all ponytail modes, skills, and commands. One-shot display, not a persistent mode. Trigger: /ponytail-help, \"ponytail help\", \"what ponytail commands\", |
| [`ponytail-review`](skills/ponytail/ponytail-review/SKILL.md) | Code review focused exclusively on over-engineering. Finds what to delete: reinvented standard library, unneeded dependencies, speculative abstractions, dead flexibility. One line |

### `research` (2)

| Skill | Mô tả |
|---|---|
| [`oss-fork-research-plan`](skills/research/oss-fork-research-plan/SKILL.md) | Use when cloning a product via OSS fork research plan. |
| [`social-channel-research`](skills/research/social-channel-research/SKILL.md) | Use when researching a social creator page or share URL. |

### `runtime-wrappers` (4)

| Skill | Mô tả |
|---|---|
| [`claude-mem`](skills/runtime-wrappers/claude-mem/SKILL.md) | Reference only. thedotmack/claude-mem (Apache-2.0) GitHub about-text lists Hermes, but cloned source has no Hermes installer (Claude/OpenCode/OpenClaw only). Do not enable a second |
| [`codegraph`](skills/runtime-wrappers/codegraph/SKILL.md) | Use when a local code knowledge graph would cut repo-read tokens. Upstream colbymchenry/codegraph (MIT) claims Hermes support. Do not install the daemon unless the user asks. |
| [`repomix`](skills/runtime-wrappers/repomix/SKILL.md) | Use when packing a repo into one AI-friendly file for review or handoff. CLI: npx repomix. Upstream yamadashy/repomix (MIT). |
| [`repomix-explorer`](skills/runtime-wrappers/repomix-explorer/SKILL.md) | Analyze or explore a codebase (remote or local repository) by packing it with the Repomix CLI, then reading and searching the generated output. Use when the user wants a high-level |

### `software-development` (3)

| Skill | Mô tả |
|---|---|
| [`moneyprinter-vietnamese`](skills/software-development/moneyprinter-vietnamese/SKILL.md) | Use when deploying Vietnamese MoneyPrinterV2 workflows. |
| [`oss-fork-baseline`](skills/software-development/oss-fork-baseline/SKILL.md) | Use when executing P0 baseline for an approved OSS fork. |
| [`vibe-coding-course`](skills/software-development/vibe-coding-course/SKILL.md) | Use when applying the saved Vibe Coding course. |

### `superpowers` (11)

| Skill | Mô tả |
|---|---|
| [`brainstorming`](skills/superpowers/brainstorming/SKILL.md) | You MUST use this before any creative work - creating features, building components, adding functionality, modifying behavior, or planning anything new, in software or out of it (a |
| [`diagnosing-superpowers`](skills/superpowers/diagnosing-superpowers/SKILL.md) | Use when a superpowers session went wrong and your human partner wants to know why — repeated work, ignored plans, stumbles, poor results, a skill that didn't fire, "it took too lo |
| [`dispatching-parallel-agents`](skills/superpowers/dispatching-parallel-agents/SKILL.md) | Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies |
| [`executing-plans`](skills/superpowers/executing-plans/SKILL.md) | Use when executing an implementation plan in the current session as the implementer yourself — your human partner chose inline execution, or no subagent tool is available |
| [`finishing-a-development-branch`](skills/superpowers/finishing-a-development-branch/SKILL.md) | Use when implementation is complete, all tests pass, and you need to decide how to integrate the work |
| [`receiving-code-review`](skills/superpowers/receiving-code-review/SKILL.md) | Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionable - requires technical rigor and verificati |
| [`subagent-driven-development`](skills/superpowers/subagent-driven-development/SKILL.md) | Use when executing implementation plans with independent tasks in the current session |
| [`using-git-worktrees`](skills/superpowers/using-git-worktrees/SKILL.md) | Use when starting feature work that needs isolation from current workspace or before executing implementation plans - ensures an isolated workspace exists via native tools or git w |
| [`verification-before-completion`](skills/superpowers/verification-before-completion/SKILL.md) | Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any succ |
| [`writing-plans`](skills/superpowers/writing-plans/SKILL.md) | Use when you have a spec or requirements for a multi-step task, before touching code |
| [`writing-skills`](skills/superpowers/writing-skills/SKILL.md) | Use when creating new skills, editing existing skills, or verifying skills work before deployment |

### `trading` (7)

| Skill | Mô tả |
|---|---|
| [`crypto-radar`](skills/trading/crypto-radar/SKILL.md) | Real-Time Crypto Market Intelligence, Multi-Timeframe Technical Scanner (15m/1h/4h/1d RSI, EMA20/50, ATR), Orderbook Imbalance, Hyperliquid Top Open Interest & Funding Rate Radar, |
| [`freqtrade`](skills/trading/freqtrade/SKILL.md) | Freqtrade (freqtrade/freqtrade v2026.11 + FreqUI 3.3.0 + TA-Lib) — 24/7 Crypto Automated Trading Bot, Backtesting, Hyperopt & FreqAI Machine Learning Engine. Use when downloading h |
| [`hkuds-vibe-trading`](skills/trading/hkuds-vibe-trading/SKILL.md) | HKUDS/Vibe-Trading (vibe-trading-ai v0.1.19) — Multi-Agent Finance & Crypto Trading Workspace, Alpha Zoo (478 alphas across 5 libraries), Swarm Research Teams (30 presets), Paper T |
| [`risk-guard`](skills/trading/risk-guard/SKILL.md) | Hard Risk Guardrails, Position Sizing Calculator & Emergency Kill Switch for Ai trading. Enforces max risk per trade (<= 2%), minimum R:R ratio (>= 1.5), max leverage (<= 5x), and |
| [`trade-journal`](skills/trading/trade-journal/SKILL.md) | SQLite Trade Journal & Post-Mortem Memory Ledger for Ai trading. Logs every recommended trade signal (Entry, SL, TP, Leverage, Thesis), evaluates open signals against real-time Bin |
| [`tradingagents`](skills/trading/tradingagents/SKILL.md) | TauricResearch/TradingAgents (v0.7.1) — Multi-Agent LLM Financial & Crypto Trading Firm Framework. Simulates a full institutional trading desk with parallel Analysts (Technical/Mar |
| [`vibetrading`](skills/trading/vibetrading/SKILL.md) | Build, validate, backtest, analyze, and deploy cryptocurrency trading strategies using VibeTradingLabs/vibetrading (v0.4.0). Use when: (1) generating trading strategies from natura |

### `video` (1)

| Skill | Mô tả |
|---|---|
| [`dung-video-talking-head`](skills/video/dung-video-talking-head/SKILL.md) | Use when có sẵn một video người nói quay dọc 9:16 (HeyGen, avatar AI, quay điện thoại, talking-head) và cần dựng thành video ngắn TikTok/Reels/Shorts có phụ đề động tiếng Việt, chữ |
