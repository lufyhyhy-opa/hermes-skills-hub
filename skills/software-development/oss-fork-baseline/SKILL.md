---
name: oss-fork-baseline
description: "Use when executing P0 baseline for an approved OSS fork."
version: 1.0.0
author: LinTech Implementation
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [oss-fork, baseline, worktree, node-engines, production-smoke, license-gate, media-export]
    category: software-development
    related_skills: [oss-fork-research-plan, executing-plans, using-git-worktrees, verification-before-completion, harness-engineering-trust-pyramid]
---

# OSS Fork Baseline (P0)

Run **Phase 0 baseline** and the **first daily-driver packaging smoke** of an OSS product clone after `oss-fork-research-plan` handoff. Goal: pinned tree builds; a **production** path proves import → persist → reopen → export with evidence; optional internal packaged app smoke proves the embedded server boots outside the source tree — without claiming distribution or feature parity.

Load with `executing-plans`, `using-git-worktrees`, `verification-before-completion`. Keep `oss-fork-research-plan` for claim classes and license rows.

## When to Use

- User approved the Master Plan / WBS and says implement / chạy P0 / baseline / tiếp tục theo WBS
- Research package exists with pinned SHA, engines range, LICENSE-REGISTER, acceptance tests
- First coding session on the fork, or the next WBS phase after a green P0 report

Skip for pure research (no install/build). After P0 is ledgered complete, do not re-run the whole baseline — resume at the next incomplete WBS id with its acceptance tests.

## Standing rules

1. **Audited SHA is the tree** — package `version` / release tag can point elsewhere; `git rev-parse HEAD` must equal the plan SHA before any install.
2. **Do not mutate the audit checkout** — bare mirror + linked worktree (or fresh clone) for implementation; leave the research audit tree clean.
3. **Do not change global Node** — pin a project-local toolchain that satisfies `package.json` `engines`; keep host Node untouched.
4. **Internal-only until license disposition** — SBOM inventory ≠ clearance; AGPL/copyleft notices, Remotion tier, FFmpeg flags, model/weight rows stay blocked for public distribute until written disposition.
5. **Production smoke, not Vite dev** — serve built assets through the product's production/embedded server path; record origin, data dir, and receipt paths.
6. **Decode with product binaries** — host `ffmpeg`/`ffprobe` on PATH may be wrappers into unrelated trees; assert with the lockfile-installed binaries under `node_modules`.
7. **Reopen needs a clean browser context** — same-page navigation is not persistence proof; second context (or full restart) must reload the saved project.
8. **Product data-dir env ≠ Electron userData** — product data-dir env isolates project SQLite/media only. Packaged app launches must also set Electron `--user-data-dir` under the execution folder. A default `~/Library/Application Support/<app>` profile is outside the worktree; packaged startup may delete older versioned compositor bundles there. Never open a packaged binary for QA without a verified isolated user-data dir.
9. **Internal package ≠ ship** — prefer `--dir` / local unpack over installer publish; ad-hoc codesign may verify while Gatekeeper/`spctl` rejects; that is expected and is not distribution clearance.

## Procedure

### 1. Preflight from the research package

1. Read `MASTER-PLAN.md` Phase 0, `WBS.csv` P0 rows, `LICENSE-REGISTER.csv`, acceptance notes.
2. Confirm disk free is enough for install + build + models later (fail closed if under plan threshold).
3. Record host facts: OS/arch, free disk, host Node (informational only), Chrome/FFmpeg availability.

### 2. Isolated tree on the pinned SHA

```bash
# From a durable project root (not the research scratch audit path):
git clone --bare --no-hardlinks <audit-or-url> upstream.git
git --git-dir=upstream.git remote add upstream <canonical-url>   # if missing
git --git-dir=upstream.git worktree add -b <fork-branch> app <PINNED_SHA>
cd app && test "$(git rev-parse HEAD)" = "<PINNED_SHA>"
test -z "$(git status --porcelain)"
```

Keep `upstream` remote on the worktree. Do not start feature commits on `main` of the audit clone.

### 3. Engine-correct toolchain (Node example)

1. Read `engines.node` (or equivalent).
2. Download the matching official binary tarball into `toolchain/`, verify SHA256 against the dist SHASUMS file, extract beside the project.
3. All product commands use `PATH=<toolchain>/bin:...` and an isolated `HOME` / npm cache under the project — never the interactive shell's global Node alone.

### 4. Native prerequisites named by the plan

- Install only what the baseline gate lists (cmake for source builds, Chrome for headless, etc.) into project-local paths when possible.
- Prefer plan env overrides (e.g. `OPENCHATCUT_WHISPER_CLI`) over forcing optional Metal/GPU paths when baseline only needs a runnable binary.
- Record binary SHA256 and `--help` probe output in the execution folder.

### 5. Install + production build

```bash
env -i HOME=<iso-home> PATH=<tool-node>:/usr/bin:/bin \
  npm_config_cache=<project>/toolchain/npm-cache \
  npm_config_registry=https://registry.npmjs.org \
  npm ci --no-audit --no-fund
# then:
env -i HOME=<iso-home> PATH=<tool-node>:/usr/bin:/bin \
  OPENCHATCUT_DATA_DIR=<execution>/build-data \
  npm run build   # or the package's production build script
```

Capture full logs + exit codes. After `npm ci`, if the package manager reports blocked install scripts (`allowScripts` / similar), **check the real binary paths** the smoke needs (`ffmpeg-static`, platform ffprobe, electron, esbuild, onnxruntime). Approve only the packages required for the gate and re-run install for those; do not treat a green `npm ci` exit as proof every native postinstall ran.

### 6. License / SBOM snapshot (P0 gate, not ship)

1. Generate lock + installed SBOMs (`npm sbom` or equivalent).
2. Refresh LICENSE-REGISTER rows for code, Remotion/major media SDK at **exact version**, bundled FFmpeg, fonts, models.
3. State distribution purpose: **internal trial** vs distributed/hosted. Unresolved rows keep `blocked` / `review_required`.
4. Never report “ready to sell/ship” from a green build alone.

### 7. Runtime map (I1–I6 style)

Trace once from real paths: UI → editor store/commands → persistence → preview composition → export path → MCP/agent bridge → workers. Write the map into the baseline report; mark source-present vs runtime-proven separately.

### 8. Production smoke + decode

Minimum media-editor pattern (adapt names to the product):

1. Start production/embedded server with isolated `HOME` + data dir + loopback bind.
2. Playwright/Chromium against that origin only — abort non-loopback hosts so “offline-ish” UI still loads.
3. Create project → import fixture → place on timeline → leave editor (flush save) → **new browser context** → reopen → assert clip/doc still present.
4. Export configured duration/size/FPS → save artifact.
5. `ffprobe`/`ffmpeg -xerror` with **node_modules product bins**; assert duration within ±1 frame, codec, resolution, frame count; keep source fixture SHA unchanged.
6. Write `receipt.json` (origin, project id, HTTP statuses, blocked hosts, export engine badge, hashes, elapsed).

UI tip: many locales keep Chinese (or other) source strings as i18n keys — wait for locale dict load and prefer `get_by_role(..., name=…)` / `title` / `aria-label` after the English (or target) dictionary is active, not raw key guesses from source alone.

Details: `references/media-editor-smoke.md` (HTTP Playwright path and packaged Electron path).

### 9. Baseline report + ledger

Write `execution/p0/P0-BASELINE-REPORT.md` (or plan path) with: SHA, branch, toolchain versions, commands, license decision, smoke receipt path, explicit **not done** list. Mark WBS P0 rows complete only with those paths. Stop or continue to Phase A per user scope — do not auto-publish or auto-spend.

### 10. Phase A-01 packaged app smoke (when WBS requires it)

1. Prefer the product's local package script that builds production assets + main process + render bundle + **directory** output (no publish channel).
2. Assert the app bundle contains production `dist/`, render serve bundle, and headless browser/compositor resources the export path needs.
3. Launch only with isolated env:
   - product data dir under `execution/A-01/`
   - Electron `--user-data-dir` under the same execution tree
   - isolated `HOME` / cache when the harness allows
4. Prefer the product's built-in packaged smoke flags (no-window API/MCP/preload checks, optional still-frame render) and require an explicit pass marker plus exit 0.
5. Confirm process argv actually contains the isolated user-data path before trusting isolation. If a launch ever resolves to the host Application Support profile, kill it and fix isolation — do not continue import/export there.
6. Write `execution/A-01/A-01-REPORT.md` with package path, smoke command, isolation paths, codesign/Gatekeeper status, and remaining WBS blockers.

## Pitfalls

- **Tag ≠ tree** — always re-check SHA after clone/worktree; package version can name a different commit.
- **Global Node drift** — host Node outside `engines` will fail or silently use wrong toolchain if PATH is not isolated.
- **Dev server smoke** — Vite/dev profile success does not close a production baseline gate.
- **Same-tab reopen** — memory/state can fake persistence; require clean context or process restart.
- **PATH ffprobe lies** — wrapper scripts can point at another project's compositor; hash and invoke lockfile bins.
- **SBOM greenwash** — counting components does not clear AGPL source obligations, Remotion company tier, or GPL FFmpeg flags.
- **Named AI route ≠ algorithm** — denoise is not stem separation; FaceDetector is not beauty landmarker; do not mark D-feature tasks done from dependency presence.
- **External update checks** — block or tolerate non-loopback calls in smoke; do not treat them as product failures if the core path passes.
- **DATA_DIR alone is not Electron isolation** — project DB can be isolated while Chromium profile still lands in the default Application Support path; packaged prepare steps may prune versioned bundles there. Always set `--user-data-dir` under execution for QA launches.
- **Port memory file location** — if the server reuses last port from a profile path under `HOME`, write the pin file where that profile actually resolves; a pin under the wrong HOME is ignored and the canonical port wins.
- **Blocked install scripts** — a successful `npm ci` can still leave electron/ffmpeg/onnx unbuilt when install scripts are gated; probe binaries before smoke.
- **Ad-hoc sign ≠ Gatekeeper** — deep codesign verify can pass while `spctl` rejects; record both; never treat that as notarized ship readiness.

## Verification checklist

- [ ] `HEAD` equals plan SHA; worktree branch named; audit checkout clean
- [ ] Product Node/runtime matches `engines`; global runtime unchanged
- [ ] `npm ci` + production build exit 0 with logs saved; smoke-critical native bins exist on disk
- [ ] SBOM + license register updated; distribution = internal unless disposition says otherwise
- [ ] Production server smoke: import/save/reopen/export evidence on disk
- [ ] Package-local decode asserts duration/codec/size; receipt JSON present
- [ ] If A-01 in scope: packaged app built internally; smoke used isolated `--user-data-dir`; pass marker + exit 0
- [ ] Report states what was **not** run (full test suite, models, MCP E2E, notarize/ship)
