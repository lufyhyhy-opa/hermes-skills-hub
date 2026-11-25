# Capital → target cash (small personal capital)

Use when Anh Huy states starting capital and a cash target ("vốn X, kiếm về Y") or an explicit monetize-with-limited-cash brief. This is a **sales + delivery ops plan**, not investment advice and not a guaranteed return.

## Procedure

1. **Parse the target literally, then split meanings**
   - Confirmed: starting capital + currency + any explicit bans.
   - Ambiguous "Y": treat separately as (a) ending total usable cash, (b) incremental profit, (c) gross revenue. Default working assumption only if needed; label `GIẢ ĐỊNH`; never claim user chose it.
   - Horizon, hours available, warm list, invoice/tax status: unknowns until confirmed.

2. **Write `decisions.json` first**
   - `confirmed` / `working_assumptions` / `unknowns` / `boundaries`.
   - Boundaries default: no spend, no public post, no third-party contact by the agent; deposits ≠ earned profit; reserves ≠ tax ruling; `MARKET_VALIDATION=NOT_VALIDATED` until paid proof exists.

3. **Tree of 3 paths (min)**
   - Productized service from existing skills (typical default for small cash + delivery capability).
   - Broker/affiliate only if a verified network already exists; otherwise mark BLOCKED for forecasting.
   - Digital product/workshop only if audience or distribution already exists; otherwise time-to-cash usually fails the horizon.
   - Reject inventory-heavy or ad-first paths until one paid conversion or equivalent signal exists.

4. **Anchor public commodity prices before locking price**
   - Fetch live public quotes for the commodity layer (e.g. single landing-page build).
   - If the proposed price is a large multiple of the commodity build price, the offer must sell **operations** (pipeline, scripts, SLA, training, milestone delivery) — not "a page".
   - Provide a **feature/terms downsell** (narrower scope), never naked same-SKU discount as the only path.

5. **Build the cash model in code (not mental math)**
   - Keep one generator script as source of truth; regenerate CSV/JSON from it. Never hand-edit scenario totals in prose alone.
   - Columns per client count `0..N`: gross revenue, direct cost, fixed launch cost, earmarked reserves, ending cash after reserves, net vs start, optional owner-labor accounting.
   - Unit contribution = price − direct − (reserve rates × price).
   - Clients needed = ceil((target_total − capital + fixed) / unit) when fixed is spent.
   - **Separate cases that must not share one row:** `no_launch`, `stop_loss_pre_sale` (tight burn only), `full_fixed_zero_sale_stress` (violates stop-loss), and `1..N fully collected`.
   - **Event ledger reconciliation (hard gate):** for every timeline event, `bank = prior + gross_in − direct_out − fixed_out` with **startup charged once**. Assert `free_cash = bank − reserve_pool`. Assert final free cash equals the matching full-collection scenario row. If docs print different 3/4/N-client totals than JSON, the package fails — fix generator/docs together.
   - **Horizon:** every collection milestone day ≤ inclusive horizon; SLA in business days from complete inputs; pilot acceptance before batch expansion; concurrent active jobs ≤ capacity cap; hours for N clients ≤ owner capacity or mark scenario `capacity_feasible=false`.
   - Deposits: track unearned until acceptance; receivables after acceptance unpaid; spendable after obligations = bank − reserve − unearned − committed delivery cost.
   - Refund stress: if reserve pool < one full refund after directs are spent, cap parallel jobs and keep deposit-before-work.
   - Ship a `scripts/verify_package.py` (or equivalent) that fails on: timeline double-start burn, horizon overrun, doc/JSON number drift, missing stop-loss row, capacity mislabel, WBS finish-to-start violations.

6. **Offer pack (S0–S7 compressed)**
   - MARKET_CARD → OFFER_SPEC with exclusion list → MONEY_MODEL (attraction audit → core → scope downsell → continuity parked) → LEAD_PLAN (one Core Four) → CLOSE outline → FUNNEL + tools customer pays vendors for → SCOREBOARD + kill criteria.
   - Guarantees: technical/test-lead only unless evidence supports outcome guarantees. No revenue/ads guarantees inside the core SKU.
   - Define **qualified conversation** as problem confirmed + decision-maker present + price/scope reaction — social replies do not count toward the kill threshold.

7. **Operating guards**
   - Pre-first-sale cash burn ceiling (tight).
   - Total launch cash ceiling.
   - Volume kill: defined approaches + **qualified** conversations with zero paid → revise offer/ICP or stop; do not add ads to "fix" silence.
   - Ads remain parked until one paid order or a stated demo threshold.
   - Max parallel deliveries from owner hours and SLA.
   - Log owner hours including post-handover support; stop new sales if SLA slips on active jobs.
   - Lock vendor/direct quotes before promising delivery dates — ceiling ≠ confirmed COGS.

8. **Red-team before handoff**
   - One pass: path choice / WTP / differentiation vs commodity.
   - One pass: cashflow, capacity, deposit-vs-earned, reserve sufficiency, arrears, timeline-vs-horizon.
   - Each finding: PASS | NEEDS_REVISION | BLOCKED + minimal fix. Do not score market validation high without paid evidence. Document QA pass ≠ market pass.

9. **Ops pack after model green (when user wants runnable kit / "nâng cấp")**
   - `templates/`: scope-contract, discovery-15m script, delivery checklist, one-page proposal HTML.
   - `ops/`: multi-sheet cash+pipeline workbook (Dashboard / Pipeline / contracts / cash log / scenarios / hours), local ops dashboard HTML (Monitor surface), exec deck HTML 16:9 + PPTX with action titles and the verified cash table.
   - Keep MODEL rows labeled reference-only inside the cash log; actual transactions go in a separate block.
   - Demo landing may link the one-pager; lead capture stays localStorage/CSV unless production is authorized.
   - Package zip + content hashes; mirror `~/marketing-plans/{slug}/` and Desktop sell-pack when that path is in use.

10. **Deliverables layout**
   - `~/marketing-plans/{slug}/`: `decisions.json`, `research.md`, `offer_pack.md`, `action_plan_*.md`, `wbs_tasks.csv`, `wbs_cash_scenarios.csv`, `model_scenarios.json`, `final_plan.md`, `progress.md`, `qa_report.json`, `scripts/build_model.py`, `scripts/verify_package.py`, optional `demo/`, `templates/`, `ops/`.
   - Optional Desktop project mirror for open-in-finder convenience.
   - Demo lead forms stay local (no production collection) unless explicitly authorized.

11. **Handoff language**
    - Lead with path + math table + stop-loss + open decisions + paths to ops files.
    - State clearly: plan ≠ validated demand ≠ guaranteed profit; ending cash includes starting capital unless labeled otherwise.
    - Agent does not spend, publish, or message third parties without an explicit order.

## Pitfalls

- Do not treat a best-case full-pay N-client row as the base forecast — mechanism: arrears, refunds, and zero-sale launch burn move ending cash below the headline row.
- Do not print scenario tables in Markdown that disagree with the model file — mechanism: hand-copied totals drift after generator fixes and become false executive numbers.
- Do not subtract launch fixed cost twice in a timeline (once as opening adjustment and again as an event) — mechanism: free cash and min-cash look artificially worse and fail reconciliation with the scenario row.
- Do not schedule final collections past the inclusive horizon and still claim the target met inside the period — mechanism: uncollected milestones are not cash.
- Do not collapse stop-loss pre-sale burn with full-fixed zero-sale stress into one "0 clients" row — mechanism: operators cannot see the protected floor they should actually hit.
- Do not expand past pilot until pilot hours and directs are measured — mechanism: 10h/job ceilings are assumptions until timed once.
- Do not spend annual SaaS from capital before the first paid client when a free/starter tier or customer-paid vendor path exists — mechanism: fixed burn lowers the floor before revenue arrives.
- Do not scrape or mass-message contacts; only channels the operator is allowed to use — mechanism: illegal/unwanted outreach is both a legal and list-quality failure.
- Do not call internal council auto-approve or regression-green a substitute for market validation — mechanism: document quality can be high while WTP remains unknown.
