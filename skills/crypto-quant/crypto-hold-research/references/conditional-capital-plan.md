# Conditional capital plan (hold shortlist → buy/sell rules)

Use when the user supplies total capital and wants concrete buy/sell sizing from a hold research shortlist. Research-only: no wallet connect, no live orders, no auto monitor unless the user separately requests execution tooling.

## Inputs to collect once

| Field | Why |
|-------|-----|
| Capital currency + amount | Budget math |
| Idle vs borrowed / near-term cash need | Blocks leverage and full deployment |
| Horizon (e.g. 12–24m) | Time stops / review dates |
| Max acceptable loss (planning) | Portfolio NAV brakes — not a guaranteed fill |
| Existing holdings + venue | Avoid double-count; no secrets/API keys |

Default if user is silent after clarify: **spot only, no margin/futures/borrow**, cash reserve ≥50%, fail-closed unlock gates stay on.

## Portfolio skeleton

1. **Cash reserve** — keep outside the exchange sleeve when possible; USDT on exchange is not risk-free cash.
2. **Crypto budget ceiling** — remainder split across gate-cleared names only as **ceilings**, not mandatory fills.
3. **Watchlist remainder** — shortlist names still missing unlock/fundamentals get **zero budget** until verified.
4. **Priority order** — research priority (e.g. BTC → ETH → …), not market-cap rank as automatic weights.

Do not move unused budget from coin A to coin B without an explicit user change.

## Entry mechanics

- Print **technical zones from closed candles**, labeled technical references not fair value.
- **Stand aside at snapshot** when price is outside zones or daily structure remains bearish without a defined trigger — do not chase full deployment to “put money to work”.
- Give the plan an **expiry date**; do not silently extend zones after expiry.
- Default tranche split on a ceiling: **40% / 30% / 30%** with minimum spacing (e.g. ≥7 days) between stages.
- Stage-1 trigger example: price in zone + closed 4h higher-low structure with break of the intervening swing high, then retest — not RSI-oversold alone.
- Later stages still require zone + structure + risk-cap room; stage-3 may add closed daily close above EMA20. If price leaves the zone, **skip** — never raise the ceiling to chase.

## Risk math

Run `risk-guard size` **per asset** with:

- `--leverage 1` for spot hold plans
- entry at zone **cap** (worst case in zone) unless a tighter live limit is known
- SL and first TP with R:R ≥ desk minimum (usually ≥1.5; hold plans often print 2R/3R/4R ladder)

Then compute **portfolio open cost-to-stop** after fees/slippage assumptions:

- Per-asset open risk ≤ min(absolute floor, ~2% current NAV) unless user sets tighter
- Portfolio open risk ≤ min(absolute floor, ~3% current NAV) unless user sets tighter
- Intraday NAV drop ≥ ~4% of day-start NAV → freeze new buys / cancel unfilled buys

If full ceilings at original stops breach the portfolio cap, **mark full deployment blocked**. Scale down or skip adds; **never loosen stops to fit budget**.

Quantity (local fiat → coin):

```text
qty = fiat_budget / actual_USDT_fiat_ask / coin_USDT_fill / (1 + actual_buy_fee)
```

Label mid-market USD/fiat FX feeds as **non-executable references**. Replace fee/slip assumptions with venue quotes before any real order.

## Exit mechanics

Define **Q0** = total units of that asset before the first profit take.

| Event | Size |
|-------|------|
| TP1 / TP2 / TP3 | Fixed fractions of **Q0** (default 30% / 30% / 20%) |
| Runner | Remaining Q0 fraction (default 20%) on trail |
| Stop hit | **100% of remaining** on that asset; overrides all TPs |

After TP1: freeze new adds on that asset; raise stop on remainder to at least fee-adjusted average cost + small buffer, never below market, never lower a raised stop. From TP2: trail (e.g. 20% under highest closed daily high since TP2) floored by the current stop — trail may exit before TP3.

Proceeds return to **cash reserve**; do not auto-rotate into another alt inside the same plan.

## Portfolio NAV brakes

NAV = cash + marked crypto sleeve after costs (do not double-count sold cash).

| Condition | Action |
|-----------|--------|
| NAV hits planning soft floor (e.g. capital − half stated loss tolerance) | Freeze buys, review |
| NAV hits harder floor (buffer before full stated loss tolerance) | Exit remaining crypto sleeve as plan rule — still no fill guarantee |
| Horizon mid-review | Underwater + below long MA → partial reduce |
| Horizon end | Exit remainder unless user approves a replacement plan |

Always stress: crypto sleeve −40% / −50% / −100% vs stated loss tolerance so the user sees when the tolerance is incompatible with full deployment.

## Logging and delivery shape

- Vietnamese tables when the user works in Vietnamese: snapshot → ceilings → buy triggers → risk caps → sell ladder → NAV brakes → execution status.
- Persist machine-readable ceilings/stops/TPs (JSON/CSV) under the session scratch when useful.
- Journal rows for unexecuted plans: status **PLANNED** (or thesis `not_an_order=true`) in a **separate DB** from live OPEN fills when possible.
- Closing line must state: **no orders placed / no bot armed** unless the user explicitly asked to execute and tools actually did.
