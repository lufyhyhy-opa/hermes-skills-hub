# Operator Pack — Post-WBS Feasibility Layer

Use after a verified execution-upgrade plan (six parts + ID-keyed task register + WBS) already exists and the user asks to continue upgrading feasibility/ops — not to replace strategy.

## When

- Master plan + WBS already pass structural QA.
- User wants channel priority, calendar, automation specs, capacity proof, or operator handoff.
- Scope remains planning/demo: no publish, OAuth, cron, contact collection, or spend.

## Deliverable set (one pack, one version)

| Artifact | Role |
|---|---|
| `operator_pack.json` | Single source: channels, briefs, calendar, loops, capacity model, experiments |
| Channel playbook CSV | Priority tier, role, formats, cadence, KPI, stop condition, activation gate |
| Content briefs CSV | Angle research only — label `RESEARCH_NOT_PUBLISHABLE`; no final captions |
| Placement board CSV | One row per funded package-day; enforce core + optional caps |
| Automation contracts JSON | Four separable loops (intake / repurpose / publish-stage / weekly-learn), status `INACTIVE` |
| Capacity lab model | Role-hour buckets; blank input → `UNKNOWN_CAPACITY`; `live_ready` always false until named non-overlap assignment |
| Experiments CSV | Sequential only; one active hypothesis at a time; kill/advance rules |
| Weekly report template JSON | Null defaults; no invented baselines |
| Offline queue simulator | Terminal states only; `side_effect_performed=false` always |

Preserve the prior plan version as archive. Bump `plan_version` (e.g. operator-pack). Generate site downloads and the browser surface from the same pack; do not hand-edit exports.

## Command Center layer (after operator pack is live)

Use when the user wants the ultimate/ops-complete upgrade on a verified operator pack — still planning/demo, still freeze strategy WBS/package caps.

| Artifact | Role |
|---|---|
| `command_center.json` | Single Operate source: readiness gates, staffing model, package factory, multi-week ops calendar, M3 receipt, kill switches |
| Readiness gates CSV | P0 product/rights/consent/account/independent QA/staffing/UAT/final command (+ optional-period receipt); default UNKNOWN or NOT_ALLOCATED; `blocks_live` explicit |
| Staffing allocator (pure JS) | Named person → role-pool hours; blank people → `UNKNOWN_STAFFING`; same person with producer+independent QA hours → `INDEPENDENCE_BLOCKED`; fit still `live_ready=false` |
| Package factory (pure JS) | Instances/QA/placement caps from the frozen package contract; output always `PROPOSED_NOT_PUBLISHABLE` |
| Multi-week ops calendar CSV | Proposed week themes tied to foundation/canary/repeat/decision windows; no auto-publish |
| M3/optional receipt + kill switches | Receipt starts NOT_ALLOCATED; kill switches default OFF/unarmed |

**Readiness rule:** even if every gate is forced PASS in a simulator (`GATES_PASS_ASSUMED`), emit `live_ready=false` — gate green is not final command, destination UAT, or spend authorization.

**Staffing rule:** demand buckets must use the same capacity period and role list as the operator pack; do not seed people from demand. Independence is identity-based, not “enough total hours.”

**Site surface:** primary composition is **Operate** (gates/staffing/factory/ops), with the frozen WBS browser retained. Archive the prior live operator HTML under its exact version name before promote.

**Ship order addition:** TDD command-center shape + readiness/staffing/factory modules → generate pack/exports → council QA with finding→remediation evidence and `execution_permission=false` → render Operate UI from the same JSON → allowlist new public downloads → deploy → HTTP byte-match every advertised route including archives → browser: gate blocking, independence block, factory instance count, exact-ID task filter, mobile overflow.

## Channel tiers

Assign every channel exactly one tier and a stop condition:

- **primary** — funded first destination after canary
- **discovery** — test next, needs comparative experiment before promotion
- **repurpose** — same master, extra placement cost counted
- **foundation** — owned assets/SEO/community infra, not daily posts
- **optional** — only if capacity surplus + explicit allocate receipt
- **parked** — designed but not in current ceiling

Do not let a discovery label imply product-channel fit. Keep platform API limits as capability facts, not workarounds to invent.

## Placement board rules

1. Board length = funded repeat window only (e.g. 28 days for packages in that window), not the whole 90-day horizon.
2. Cap core placements and optional group/community rows separately; assert counts in tests.
3. One multi-image post = one placement. Cross-post ≠ new original.
4. Leave unfunded days empty rather than padding vanity rows.
5. Board rows reference package IDs from the frozen register — never invent new package IDs here.

## Capacity and effort reconciliation

- Start from the source planning model and task register. Reconcile task effort + standing service by the exact budget period; record the task-level role/hour source, not only a top-line total.
- Label the production/placement window separately from the full budget/resource window. For example, if production runs D31–D58 but a resource decision is D59–D60, all M2 availability inputs and M2 fixed effort cover D31–D60. Never compare 28-day availability to 30-day demand.
- Build a ledger `task_id → work component → role pool → low/high hours → days/package → treatment`. Each component counts once; package rows plus fixed rows plus standing service must reconcile to the source model totals and task totals.
- Decompose aggregate package effort across role pools only as an explicit proposed allocation; keep reviewer hours distinct, and keep writer/editor and independent reviewer identities separate. If staffing identities or independence are unknown, label the split unverified and keep QA blocked. When the source model only attributes whole packages to one responsible role (e.g. producer), keep that legacy view labeled non-additive; the pool decomposition is an accounting proposal, not a second stack of hours on top of the legacy totals.
- Model fixed work and standing service separately from per-package work. When package count drops, fixed work does not scale down; reschedule it within the period or mark infeasible. Test the one-package case specifically.
- For every added operator record, name its parent task, what prior artifact/work it replaces, setup vs recurring effort, and what is conditional/unestimated. Preserving task IDs or package caps is not evidence that extra reporting, experiments, exception handling, or automation development fits inside the estimate. Unknown additional effort stays `CONDITIONAL_NOT_ESTIMATED`; re-estimate and reduce scope/defer before activation.
- Roles use non-overlap buckets. UI/model empty inputs → `UNKNOWN_CAPACITY`; never seed from demand. Compare available and demand over the same named period; require total and each role bucket.
- Outputs: `FITS_ASSUMED_HOURS` | `SHORTFALL` | `INVALID_INPUT` | `INVALID_ALLOCATION` | `UNKNOWN_CAPACITY`. Always emit `NOT_LIVE_READY` / `live_ready=false`; modeled fit does not prove people, calendars, independence, quotes, rights, UAT, release or authorization.

## Automation contracts (planning-only)

Fill all nine loop anatomy fields. Default status `INACTIVE`.

Offline simulator allowed terminals only:

`HOLD` · `RECONCILE` · `SKIP_DUPLICATE` · `SUPPRESS` · `HALT` · `READY_FOR_MANUAL_HANDOFF` / `READY_FOR_MANUAL_REVIEW`

Forbidden until explicit final command + live UAT + destination receipt:

`PUBLISHED` · `SENT` · `SPENT` · network calls · OAuth · cron enable · CRM writes

Every simulator result sets `side_effect_performed=false` and `dispatch_allowed=false`. Schema/fixture green ≠ live permission.

**Combined blockers (required):** collect every applicable blocker for diagnostics; any blocker forbids dispatch. Primary decision precedence high→low: kill→`HALT`; unknown side-effect state→`RECONCILE` (read-only, never blind retry/send even if also suppressed/duplicate/mismatch); send without purpose consent or with suppression→`SUPPRESS`; known duplicate key→`SKIP_DUPLICATE`; other blockers→`HOLD`; no blockers→`READY_FOR_MANUAL_HANDOFF`. The primary label does not erase remaining blockers.

**Approval binding:** final approval must match exact `action`, `content_id`, `package_id`, `version`, `channel`, `destination_id`, `slot`, `payload_hash`. Separate execution flag must be exact boolean `True` (truthy 1/"true" fails closed). Missing package/destination/action fields fail closed. Valid queue states only: `queued` | `unknown` | `published` | `sent`.

Keep a machine-readable queue contract (precedence, bound fields, synthetic fixtures) next to the simulator so adapters cannot reinterpret single-condition tests as full policy.

Wire loop anatomy through `marketing-loops` continuous-content branch and `references/loop-orchestration.md`.

## Experiments and cohort reads

- Queue experiments sequentially; do not run parallel channel tests that share creative/reviewer capacity without explicit surplus.
- Each experiment defines entry criteria/T0, one variable, metric, numerator, denominator, observation window, earliest read, sample limitation, HOLD rule and next action. A board window is not evidence that the measurement cohort has matured.
- For a 7-day qualification plus 24-hour watermark, conversion cannot be read before entry-window end + 8 days; cohort activation cannot be read before the latest qualification end + 8 days. Keep open cohorts `PENDING`, missing observation/join `NOT_MEASURABLE`, confirmed zero denominator `UNDEFINED`, and absent source/baseline `UNKNOWN`; never substitute zero.
- Do not promise that a sequence of experiments fits a production calendar. Any follow-up/read after the funded period requires a separate resource receipt; absent receipt means defer, even if data technically matures.
- Primary-channel labels stay working hypotheses until a comparative experiment closes.

## Build / test / ship order

1. TDD the pack shape (channel count, brief flags, board caps, loop INACTIVE, capacity blank→UNKNOWN).
2. Create `operator_pack.json` from the frozen register + planning model.
3. Export CSV/JSON; assert parity with pack. Make downstream finalizers consume the enriched current model, not reload the earlier baseline and discard new fields. Assert the final exported capacity, effort map and period equal the canonical pack; rerun this check through the final entrypoint.
4. Implement offline simulator + capacity module; test blank/zero/invalid inputs, role bottlenecks, one-package fixed effort, ledger reconciliation and combined queue blockers. Exercise the shared pure capacity function with Node and the queue/model checks with Python unittest; zero side effects and blank≠default-fit are required.
5. Close every requested independent review lane, then create document QA with `execution_permission=false`. For each material finding, record source, accepted/pushed-back verdict, remediation and exact regression/artifact evidence. Keep subjective rubric scores reasoned and separate from machine checks; pending reviews or unresolved material findings prevent a final QA-pass label. Never hard-code a passing score from counts or unconditionally set all-remediation-applied.
6. Render site: operator panel, capacity grid, WBS browser, archive link to prior version. UI copy and inputs must use the same period name and full role list as the pack (if capacity is M2 D31–D60 with an organic pool, the lab must say that period and expose that input — do not hard-code “28 days” or a six-role subset). Before promote, archive the currently live operator-pack HTML as its own version file, not only the older strategy baseline.
7. Deploy; verify every advertised public route HTTP 200 + byte/hash match with cache-bust query, including new CSV/JSON downloads and the prior-version archive. If the host uses a deny-by-default ignore list for CSV/JSON, allowlist each new public download before deploy or the route 404s while local files look fine. Browser: filters, exact-ID, capacity blank/fit/shortfall, one-package fixed-effort demand, mobile overflow. Render the UI from the same period, roles and fixed/per-package model as the canonical pack.
8. If a material audit arrives after handover, reopen the affected QA conclusion and start a versioned correction: classify each finding, add a regression test that fails on the unfixed pack, fix source/generator, rebuild exports/site, rerun the final entrypoint, redeploy within existing authorization and read back the same targets. Preserve the factual deployment record of the older version; distinguish it from a locally tested revision. Do not label the live release corrected while changes remain local.
9. Handover: URL first, downloads, freeze list (no publish/spend/collect), open blockers (owners, P0 product proof, optional-period allocate receipt).

## Pitfalls

- Rebuilding strategy when the ask is operator feasibility or “ultimate ops” wastes the frozen register — add Command Center, do not rewrite six parts/WBS.
- Seeding capacity or staffing people from demand hours fakes readiness.
- Treating producer+independent-QA hours on one person as capacity fit hides the independence gate; block it explicitly.
- Marking briefs or factory manifests as ready-to-post copy bypasses human gates.
- Returning simulator `PUBLISHED`/`SENT` or omitting remaining blockers after a primary decision trains false automation confidence.
- Expanding board past funded package ceiling breaks budget math.
- Comparing 28-day availability to a 30-day M2 demand envelope (or scaling fixed service/decision hours with package count) invents false fit.
- UI still saying “28-day hours” after the model moved to a full budget period, or omitting a new role pool, desyncs operators from the pack.
- Verifying only the original download set after adding ledger/queue/command-center files leaves 404s undetected.
- Leaving pack generators with a permanent “output must not exist” assert blocks review remediations and versioned rewrites.
- Deploying without archiving the prior live operator/command HTML loses rollback.
- Claiming campaign start or live correction because local tests or gate overrides passed — deploy/readback ≠ execution authorization; local rN ≠ live until verified; gate PASS ≠ final command.
