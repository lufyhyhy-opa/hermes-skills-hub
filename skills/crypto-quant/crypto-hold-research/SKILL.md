---
name: crypto-hold-research
description: Use when screening or capital-planning long-hold coins.
version: 1.0.0
author: Hermes Agent — Ai trading
license: MIT
metadata:
  hermes:
    tags: [hold-research, scorecard, weekly-report, tokenomics, fail-closed]
    related_skills: [token-unlock-treasury, onchain-analysis, defi-yield, crypto-radar, risk-guard, github]
---

# Crypto Hold Research

Research and ranking only. Never connect wallets, place orders, or treat a score as a trade ticket.

## When to Use

- User wants a long-hold coin shortlist, scorecard, or “quy chuẩn đánh giá hold”
- Building/updating a weekly hold Markdown report or GitHub Actions research pack
- Choosing free data sources / unlock policy for automated screening
- Mapping GitHub repos that support hold frameworks (not trade bots)
- User gives capital + horizon + loss tolerance and asks when/how much to buy and sell from a hold shortlist (conditional capital plan)

Skip for pure short-term scalp signals, order execution, or wallet-connected bots — use `crypto-radar` + `risk-guard` instead. A capital plan still does not place orders.

## Standing rules

1. Split three questions every time: **project quality**, **token value accrual**, **entry price / timing**. A good project is not automatically a good token buy.
2. Default automation mode is **free + fail-closed**: missing critical unlock or category-required fundamental data is explicit N/A and **blocks buy-oriented actions, including STRONG ACCUMULATE and STANDARD DCA**. Keep `data_status=insufficient` separate from investment quality; use a research-only/stand-aside result, not an inferred sell recommendation for existing holdings.
3. Do not double-count float and MC/FDV as independent fair-value evidence — they largely measure the same dilution structure when supply fields are consistent.
4. ATH / 90d drawdown is **technical discount**, not proof of undervaluation or margin of safety.
5. Volume/MCap is an **activity proxy**, not executable order-book depth.
6. Drop incomplete daily/weekly candles before RSI/MA/BB/zone math.
7. Targets (including multi-x cycle targets) only if the user configured them; never invent X3–X10 promises.
8. Prefer Vietnamese weekly dashboard layout when the user works in Vietnamese: Market Pulse → master table → entry zones → weekly delta → disclaimer.
9. Local pack first. Require a named repository and authorization before a GitHub push. Treat an explicit request for a Vercel preview link as authorization to publish a sanitized report to an isolated preview project in the authenticated scope; do not replace an unrelated app or expose account configuration.
10. Label every public dashboard as **snapshot** or **live**, show the source observation time, and distinguish deployment time from data freshness. Preserve experimental model labels as model outputs, not verified investment recommendations; never imply that hosting alone enables weekly refresh.
11. Set unlock status from asset-specific, dated evidence, not from a float threshold. High circulating supply does not prove no future unlocks or issuance. Mark a VC-cliff metric `NOT_APPLICABLE` only when the asset's issuance design is verified, and track ongoing issuance separately.
12. Compare only independent real weekly snapshots produced with compatible methodology; do not call same-week reruns, scoring-rule changes, or fixture-to-live differences weekly market changes.
13. A hold shortlist or scorecard is **watchlist priority**, not a ranked buy ticket and not portfolio weights. Do not map experimental STRONG/DCA labels straight into “buy now” without live gates + risk sizing.
14. When the user asks for capital allocation (how much / when buy / when sell): produce a **conditional plan** with cash reserve, budget ceilings, entry triggers, portfolio risk caps, and exit rules — never a guaranteed P&L path. User loss tolerance is a planning stop, not an executable max-loss guarantee (gap, illiquidity, venue failure can exceed stops).

## Procedure

### 1. Clarify policy once

If unlock coverage is ambiguous, pick one and state it:

| Mode | Behavior |
|------|----------|
| **A free fail-closed** (default) | No paid unlock API; critical UNKNOWN data caps coverage and blocks STRONG/DCA until verified |
| **B free + manual unlocks** | Auto report + `unlocks_manual.yaml` rows with source URL + verified date |
| **C paid data** | Only with explicit user OK on cost |

### 2. Build or refresh the watchlist

Each row needs: `ticker`, `coingecko_id`, `binance_symbol` (if listed), `defillama_slug` (nullable), `category`, `tier` (bluechip/leader/follower), optional `target`.

Category-aware metrics:

- **l1 / native / btc**: use network-appropriate fundamentals rather than forcing protocol TVL/revenue; do not award fundamental points merely because a market price exists. Verify the issuance design before deciding whether VC-cliff unlocks apply; never convert `UNKNOWN` to `CONFIRMED_NONE` from high float alone.
- **defi / l2 / protocol**: require TVL and/or revenue when claiming fundamentals; missing both → `fundamentals_missing` flag.
- **Narrative leadership**: curated `tier` field unless a reproducible ranking is implemented.

### 3. Pull free data (stdlib/`urllib` preferred)

| Need | Source |
|------|--------|
| Price, MC, FDV, supply, 7d/30d, ATH | CoinGecko markets |
| BTC.D | CoinGecko global |
| Closed 1D/1W candles | Binance `data-api.binance.vision` klines — **exclude candle with close_time in the future** |
| TVL | DefiLlama `/protocol/{slug}` |
| Protocol revenue | DefiLlama `/summary/fees/{slug}?dataType=dailyRevenue` |
| Fear & Greed | alternative.me |
| Unlock schedules | Not assumed free; manual verified file or paid |

Always attach source + fetch timestamp on every live metric. Retry 429/5xx with backoff; exhaust → N/A, do not fabricate.

### 4. Score (100 pts, four pillars)

Default weights matching the long-hold desk:

| Pillar | Pts | Inputs |
|--------|----:|--------|
| Tokenomics / supply | 30 | One dilution metric (float or MC/FDV), unlock status |
| Fundamentals / flow | 30 | Volume/MCap activity, ΔTVL/Δrevenue when applicable, curated tier |
| Drawdown discount | 20 | % from ATH and 90d high (label correctly) |
| Trend structure | 20 | Price vs EMA50/MA200 on closed 1D and 1W |

Gates:

- `unlock_status=UNKNOWN` → cap tokenomics (e.g. ≤18/30), flag insufficient data, and block STRONG/DCA in mode A.
- Confirmed large unlock (e.g. ≥5% circ / 30d team-VC) → hard risk flag; apply gates before score-based labels.
- Missing category-required fundamentals → insufficient data, not evidence of safety or business failure.
- Compute coverage/confidence from applicable fields, freshness, indicator warm-up and verification status; do not give full coverage because one of several trend inputs exists. Coverage is not probability of profit.

### 5. Four weekly actions (no hedge language)

| Action | When |
|--------|------|
| **STRONG ACCUMULATE** | Critical data verified, score≥70, coverage high, unlock acceptable, oversold or in zone1, all configured risk gates pass |
| **STANDARD DCA** | Critical data verified, solid score and sideways/non-chasing setup; missing strong-entry conditions are not missing critical evidence |
| **WAIT FOR PULLBACK** | High quality but RSI overbought or stretched vs MA — print limit zone |
| **AVOID / REDUCE** | Confirmed adverse evidence such as a large unlock, structure break, or materially weak score with adequate data |

If critical evidence is missing, show `data_status=insufficient` and **ĐỨNG NGOÀI — THIẾU DỮ LIỆU** instead of a buy signal or an inferred instruction to sell. Keep this data-quality state separate from the four investment-action labels.

Zones from closed weekly OHLCV swings are **technical references**, not guaranteed hard support. Label them as candle-derived.

### 6. Report + automation pack

Canonical layout for a GitHub research pack:

```text
config/watchlist.yaml
config/scoring.yaml
config/unlocks_manual.yaml
src/hold_engine.py          # pure indicators + score + actions
src/data_clients.py         # free HTTP clients
src/report_md.py            # Vietnamese Markdown
src/generate_weekly_report.py
reports/weekly/YYYY-Www.md
reports/latest.md
README.md                   # embeds latest
.github/workflows/weekly-report.yml  # cron Monday 01:00 UTC + workflow_dispatch
tests/                      # unit + offline fixture e2e
```

Workflow: collect with per-source timestamps → validate completeness/coverage → score → render → commit reports/README only on diff → optional Telegram summary must not fail the job. Store one real snapshot per ISO week; exclude fixture runs from the history consumed by live reports.

For a web preview, export only public report fields into a separate static directory, preserve N/A as null, and verify unique row counts against the source. Omit invalid same-week deltas. Load `web-ui-ux-pro-max` and its static-preview deployment reference for the Vercel publication and browser checks; leave the research engine unchanged unless the user also requests a model fix.

Local reference pack (when present on this profile):
`~/.hermes/profiles/ai-trading/cache/scratch/crypto-hold-weekly/`

Integrated capital+regime desk (when present):
`~/.hermes/profiles/ai-trading/workspace/investment-desk/` — single MASTER/desk.json for 500tr plan + cycle switches + 10-coin gates. Public plan snapshot: https://crypto-500m-plan-preview.vercel.app (research scoreboard remains https://crypto-hold-research-preview.vercel.app).

Run:

```bash
python3 -m pip install -r requirements.txt   # PyYAML only at runtime
python3 -m unittest discover -s tests -v
python3 -m src.generate_weekly_report
python3 -m src.generate_weekly_report --offline-fixture tests/fixtures/sample_report.json --output-root ./test-output
```

### 7. Conditional capital plan (when user supplies capital)

Load `references/conditional-capital-plan.md` and follow it end-to-end. Minimum sequence:

1. Clarify once: idle capital vs borrowed, horizon, max acceptable loss, existing holdings, venue (no secrets/API keys).
2. Pull live `crypto-radar` + closed 1D/1W candles; state snapshot time; if price is outside zones or structure is still daily bearish without a trigger, **stand aside now** — print zones, do not chase deployment.
3. Keep a **cash reserve** (default ≥50% of capital unless user sets otherwise); assign budget **ceilings** only to coins that pass fail-closed data gates; leave insufficient-data names on watchlist with zero budget.
4. Size with `risk-guard` **per asset at 1x spot**, then enforce a separate **portfolio open cost-to-stop cap** (default ≤3% NAV / absolute VND floor the user can state). Sum of per-asset approvals can still breach portfolio risk — cut size or skip tranches, never loosen stops to fit budget.
5. Multi-tranche entries need structure triggers (not RSI alone). Profit exits as fixed % of **original Q0**; stop exits 100% of remaining on that asset and override TPs. Freeze new adds after TP1 on that asset.
6. Log conditional rows as **PLANNED / NOT EXECUTED** in an isolated journal DB or thesis field — never as live OPEN fills. State explicitly: no orders, no auto bot, no guaranteed fill on stops.
7. VND quantity formula uses **actual USDT/VND ask + venue fees**, not a USD/VND mid reference. Label FX sources as non-executable when they are.

### 8. GitHub research sources (frameworks, not signals)

When the user asks which repos to study for hold standards, prefer live verification via public API (no `gh auth` required for read):

- `DefiLlama/defillama-skills` — protocol/token/risk research workflows (MCP may need subscription)
- `DefiLlama/dimension-adapters` — fees vs supply-side vs protocol vs holders revenue
- `DefiLlama/DefiLlama-Adapters` — TVL from chain data
- `duneanalytics/spellbook` — SQL transforms for activity/holders
- `electric-capital/open-dev-data` — developer ecosystem taxonomy (canonical name after crypto-ecosystems redirect)
- `l2beat/l2beat` — L2 trust assumptions (network quality ≠ token buy)
- `crytic/slither` — static contract checks only
- AI scorecard templates — steal **checklist structure**, not default Buy labels or heavy short-term sentiment weights for hold theses

Resolve redirects with `GET https://api.github.com/repos/OWNER/REPO` and use returned `full_name` + `default_branch` before linking.

## Pitfalls

- **Fees paid by users ≠ protocol revenue ≠ holder value** — read DefiLlama methodology fields (`dailyFees`, `dailySupplySideRevenue`, `dailyProtocolRevenue`, `dailyHoldersRevenue`) before scoring “real yield”.
- **Fetch enough closed history for the requested indicator** — MA200 on 1W requires 200 closed weekly candles; otherwise report N/A and reduce coverage, because a shorter download cannot establish the long-term MA.
- **Keep safety gates stable when fixing tests** — correct inconsistent fixtures or verify an explicitly approved rule change before relaxing an extension filter, because an oversold RSI does not independently prove a stretched entry is safe.
- **Telegram/optional notify** — catch and ignore send failures so the Markdown report still lands.
- **Schedule workflows** must live on the default branch; idle public repos can see delayed crons.
- **Do not auto-fill budgets for the whole shortlist** — only gate-cleared names get ceilings; missing unlock/fundamentals keep zero buy budget under fail-closed mode, because absence of data is not clean tokenomics.
- **Do not treat full budget ceilings as mandatory deployment** — portfolio cost-to-stop can block later tranches even when each single-asset `risk-guard size` is approved.
- **Do not sell “% of remaining” on multi-TP holds** — fix exit fractions on original Q0 so position math stays stable after partials.
- **Do not present user loss tolerance as a hard ceiling the plan can enforce** — stress the crypto sleeve at −40%/−50%/total loss and say stops can gap through.
- **Match technical citations to every asset claimed** — for a multi-coin EMA/RSI table, compute from each coin’s own closed OHLCV series and cite its corresponding ticker/timeframe endpoint; a BTC-only klines URL cannot substantiate ETH/SOL/AAVE/LINK metrics. If per-asset links are too noisy, cite a published evidence artifact that preserves complete per-ticker source and candle-cutoff provenance.

## Related skills

- `token-unlock-treasury` — unlock/treasury depth
- `onchain-analysis` — MVRV/NVT/SOPR and activity
- `defi-yield` — yield sustainability vs emissions
- `crypto-radar` — live multi-timeframe + Fear&Greed scan before discretionary entries
- `risk-guard` — size any actual trade idea after research; portfolio aggregate check is separate
- `trade-journal` — log PLANNED vs OPEN distinctly
- `github` — public repo read without auth; Actions publish when authorized
- `cycle-money-flow` — regime/money-flow lens; handbook claims need live verification

## See also

- `references/scorecard-and-actions.md` — compact score/action thresholds
- `references/conditional-capital-plan.md` — capital / buy-sell plan recipe when user supplies funds
