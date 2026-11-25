# Hold scorecard and action thresholds

Compact defaults for free fail-closed long-hold screening. Override only with explicit user policy.

## Pillars (100)

| Pillar | Max | Primary inputs | Notes |
|--------|----:|----------------|-------|
| Tokenomics | 30 | float or MC/FDV (one dilution axis), unlock status | Cap ≤18 if unlock UNKNOWN |
| Fundamentals | 30 | vol/mcap, ΔTVL 7d/30d, Δrevenue 7d/30d, tier | Natives need network-appropriate evidence, not automatic points for price availability |
| Drawdown | 20 | % from ATH, % from 90d high | Label as drawdown, not fair value |
| Trend | 20 | vs EMA50/MA200 on closed 1D+1W | No synthetic warm-up |

## Unlock

| Status | Effect |
|--------|--------|
| CONFIRMED_NONE / small (<2% circ 30d) | Score only from asset-specific evidence with source, verification date and covered horizon |
| CONFIRMED_LARGE (≥5% circ 30d team/VC) | Unlock sub-score 0; apply risk gate before entry classification |
| UNKNOWN | Cap tokenomics; mark insufficient data; block STRONG and DCA in free fail-closed mode |
| NOT_APPLICABLE | Require verified issuance design showing the metric does not apply; evaluate ongoing issuance separately |

Keep UNKNOWN unchanged when the only evidence is high float, a native/L1 category or a missing API result. A disclosure of an assumption is not verification.

## Actions

| Action | Score | Other |
|--------|------:|-------|
| STRONG ACCUMULATE | ≥70 | Critical data verified; coverage high; unlock acceptable; RSI oversold or in zone1; configured risk gates pass |
| STANDARD DCA | ≥55 | Critical data verified; non-chasing setup; strong-entry timing conditions incomplete |
| WAIT FOR PULLBACK | high quality | RSI≥70 or stretched vs MA — print available reference zone; retain independent data-quality flags |
| AVOID / REDUCE | <40 or hard risk flags | Confirmed adverse evidence such as large unlock or structure break |

If evidence is insufficient rather than adverse, output `data_status=insufficient` and a research-only/stand-aside action. Do not interpret the absence of data as a sell instruction.

## Coverage and comparable history

- Count each applicable indicator separately; MA200 on 1W needs 200 closed weekly candles. Missing warm-up lowers coverage rather than becoming a zero-valued indicator or a fully covered trend pillar.
- Label coverage as data completeness, not a forecast success rate.
- Compare different real ISO-week snapshots only. Keep fixture/demo data and same-week reruns out of weekly deltas; label a changed scoring methodology before comparing scores.

## Macro note (regime, not score)

Fear&Greed + BTC.D change **bias** (quality accumulation vs reduce FOMO). They do not replace per-asset gates.

## Report columns (master table)

Rank | Ticker(sector) | Price | 7d | 30d | %ATH | Float% | MC/FDV | RSI 1D/1W | Hold | Conf | Action
