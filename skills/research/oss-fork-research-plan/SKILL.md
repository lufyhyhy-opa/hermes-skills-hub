---
name: oss-fork-research-plan
description: "Use when cloning a product via OSS fork research plan."
version: 1.0.0
author: LinTech Research
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [research, master-plan, oss-fork, product-clone, wbs, citations, evidence]
    category: research
    related_skills: [grounded-citations, writing-plans, executing-plans, oss-fork-baseline, huy-intent-and-gold-standards, autonomous-slide-council, verification-before-completion, personal-os-operations]
---

# OSS Fork Research → Master Plan Package

Turn a public product page (and optional Build Kit) plus an open-source base into an executable research package: evidence dossier, architecture decision, WBS with acceptance tests, starter prompt, and slide deck. **Do not treat the plan package as a built product.**

Load with `grounded-citations`. For Anh Huy short orders, also load `huy-intent-and-gold-standards` and run the internal council loop from `personal-os-operations`.

## When to Use

- "Đọc toàn bộ tài liệu / Build Kit rồi lập Master Plan clone"
- Product claims a stack on a named OSS editor/app and user wants fork + extend plan
- Need claim-vs-code audit before implementation

Skip when the user already approved an implementation plan and wants code — use `writing-plans` / `executing-plans`, and load `oss-fork-baseline` for Phase 0 (pinned SHA worktree, engine-local toolchain, production smoke + license gate).

## Deliverable package (minimum)

Save under a stable project folder (e.g. `~/marketing-plans/research-<slug>/`):

| Artifact | Purpose |
|---|---|
| `PROJECT.md` | Index, decisions, what was / was not executed |
| `MASTER-PLAN.md` | Architecture choice, phases, gates, red-team, sources |
| `WBS.csv` | Independently testable tasks + deps + person-days + acceptance |
| `research/RESEARCH-DOSSIER.md` | Section/panel/kit crosswalk + upstream path audit |
| `research/BUILD-KIT-CROSSWALK.csv` | Kit heading → task ids |
| `STARTER-PROMPT-V2.md` | Implementation handoff for coding agents |
| `LICENSE-REGISTER.csv` | Code/model/asset rows; unresolved stay blocked |
| `qa/ACCEPTANCE-AND-REDTEAM.md` | Fixtures, thresholds labeled as proposed until measured |
| `slides/*.{html,pptx}` | 16:9 executive deck |
| Zip of the above | Single handoff archive |

## Procedure

### 1. Capture product evidence (browser-first)

1. Open the public product URL in the browser. Do not treat truncated `web_extract` as full inventory.
2. Record **all** headings, named sections, interactive feature panels, FAQ, and any Build Kit tabs.
3. **Static page text and interactive panels can diverge** — panel-only claims (preset counts, library sizes) live in panel captures; label extraction method. Prefer saved panel JSON over a single static scrape when they conflict.
4. If kit file URLs 404, read content from the public tabs/panels and preserve text/SVG locally. Mark independent URLs as unavailable, not unread.
5. Register every retrieved URL in the citation ledger at fetch time (`grounded-citations`).

### 2. Audit the OSS base at a pinned revision

1. Clone public source to an isolated scratch path. Prefer HTTPS public clone if `gh` is logged out.
2. **Pin the audited commit SHA** (and date). Do not silently treat a release tag or `main` as the same tree. If package version equals a tag name, still verify with `git rev-parse` / `git show`.
3. Read LICENSE, README, package engines/scripts, and the concrete paths that matter (editor core, MCP session flow, AI plugins, model catalogs, geometry/vision).
4. Match licensing evidence to the pinned dependency version: compare its tag-specific license with the applicable major-version terms, and label generic pricing or upcoming-version pages separately. Record the intended internal, distributed or hosted use, redistribution/modification rights, compatibility and notice/source duties; an inventory with zero unknown rows is not distribution clearance.
5. Write a source inventory with path + SHA-256 of key files. Record the exact engine range and host constraints as **preflight gates**, not as proof the project builds.
6. **Do not install deps or run product build** unless the user asked for implementation — research plans stop at evidence + plan.

### 3. Separate claim classes

| Class | Treatment |
|---|---|
| Verified in audited source | Cite commit-pinned blob URL; path + behavior |
| Product-page / Build Kit claim | Cite page; never use as clone acceptance until remeasured |
| Author benchmark (WER, timing, dB, model MB) | Hypothesis; own fixtures + target-machine metrics |
| Code license | Not the same as model weights, fonts, LUT, SFX rights |
| Plugin name vs algorithm | e.g. "voice isolation" route may be denoise filters, not stem separation |

Never upgrade a marketing number into a WBS acceptance threshold.

### 4. Architecture decision (Tree of Thoughts)

Produce three options, e.g. fork+harden vs clean-room vs thin wrapper. Score as **relative planning estimates**, not measured engineering scores. Prefer fork when EditorCore/timeline/MCP/render already exist and the gap list is additive. Treat a thin MCP client that only sends upstream commands as a valid control; it does not inherently duplicate project state. Keep the fork baseline conditional on the planned production smoke tests.

Before estimating AI reuse, map each engine to its observed browser/server/desktop context, required adapter, model format and packaging path. Dependency presence does not establish a working runtime integration; a detector/segmenter does not establish landmarks, retouch or matting.

Lock contracts early:

- One writer / revision / undo unit for external agents
- Live **progress** UI ≠ concurrent multi-writer apply
- Preview/export shared composition
- Derived media never overwrites source
- Data directory outside code; heavy jobs serialized

### 5. Map kit pitfalls and features → WBS

1. Every Build Kit milestone and P1–Pn pitfall becomes one or more tasks with **reproduce-before-fix** acceptance when the pitfall is claimed fixed upstream.
2. Every feature panel becomes keep / extend / build-new with owner tasks.
3. WBS rows need: `task_id`, phase, deliverable, `depends_on`, `estimate_person_days`, acceptance test, scope (MVP vs Full), `execution_status=chưa thực thi` until code runs.
4. **Person-days ≠ calendar.** Report: task count, person-days, capacity model (contingency × useful-time × headcount), then a week **range**. Re-estimate after baseline phase.
5. Keep MVP dependency-closed: no MVP task depends on Full-only work without saying so. Traverse the release gate's transitive dependencies and compare them with every feature, model-license and packaging task required by that release; list optional platform/fast-path exclusions explicitly.
6. Separate feasibility spikes from production integration. Give each promised feature implementation, UI/MCP, artifact/cache/cancel and acceptance ownership after its go/no-go; a successful spike cannot close a shipped-feature gate.
7. Define each acceptance test as fixture + action sequence + observable assertion + threshold or review rubric + evidence output. Distinguish protocol tests from real-agent brief UAT. For editable-media workflows, verify the applied effect in export before undo, then verify restored state and redo/reapply separately.

### 6. Red-team and upgrade the plan

1. Find ≥5 plan holes: concurrency semantics, license gates, runtime preflight, claim leakage, media/recovery/offline tests.
2. Record the source commit and document/WBS revision supplied to each reviewer. When an asynchronous review arrives, compare its identifiers, counts and cited wording with the current files; an old review is evidence about its snapshot, not a verdict on the latest package.
3. Classify each finding as already resolved, still applicable or an intentional scope exception. Store the disposition and its owning task in `qa/`.
4. Apply remaining corrections to task acceptance and dependencies, then synchronize the Master Plan, dossier, starter prompt and project index. A prose-only response to an acceptance gap does not enforce the release gate.
5. Recompute effort and dependency checks after integration. If stronger acceptance keeps the previous estimate, label it provisional and require re-estimation after baseline evidence.

### 7. Package QA before handoff

1. `sources.py render --replace-in` then `verify --strict` on each prose deliverable (see grounded-citations strict pitfalls).
2. Cross-check internal links resolve; WBS DAG has no cycles; kit heading crosswalk covers P1–Pn and D-features.
3. Slides: HTML keyboard nav + overflow check; PPTX slide count/geometry; report native visual render separately if LibreOffice/PowerPoint missing.
4. Finish edits before packaging. Regenerate QA from the current file bytes, create a SHA-256 manifest for the canonical member list, then build a new versioned ZIP while preserving the previous release. Reopen the ZIP, check CRCs and member count, and compare every archived member with its on-disk bytes and manifest hash; this detects a stale archive after a late edit.
5. Keep verification meanings separate: citation strict checks establish ID/URL/format consistency, source hashes establish snapshot identity, HTML checks establish that representation, and PPTX geometry does not establish native visual rendering. Record each scope in the QA report.
6. Handoff states clearly: research package complete; implementation not started; next gate is isolated baseline build + ffprobe evidence (`oss-fork-baseline`).

## Pitfalls

- **Tag/version field ≠ audited tree.** Package `version` or release notes can lag or lead HEAD; pin SHA and replay tests on that SHA.
- **Static scrape misses panel claims.** Interactive feature carousels often hold the only copy of preset/library counts.
- **MCP product demo ≠ session contract in code.** Draft/review/apply plus one-writer is the safe default until race tests exist.
- **Named AI route ≠ claimed algorithm.** Read the plugin; denoise filters are not source separation; face geometry is not beauty retouch; MediaPipe presence is not RVM matting.
- **Code MIT/BSD ≠ ship weights.** Separate rows for models, RNNoise weights, fonts, LUT, SFX; blocked until provenance is written.
- **Dev smoke ≠ production package.** P9-class failures need clean-machine/install acceptance, not only local dev success.
- **Council score is plan feasibility, not product QA.** Never present 9/10 plan score as software quality.
- **Zero-babysitting does not authorize build/spend.** Research may auto-complete docs/slides; paid API calls, purchases, public posting and product dependency installation require scope authorization.

## Verification

- [ ] Product sections/panels/kit headings inventoried with capture method labeled
- [ ] Audited commit SHA recorded; tag/main not silently substituted
- [ ] Claims table separates page claims vs source-verified behavior
- [ ] WBS acceptance tests are executable and dependency-closed for MVP
- [ ] Citation verify --strict green on Master Plan + dossier
- [ ] Handoff explicitly says implementation/build not run
