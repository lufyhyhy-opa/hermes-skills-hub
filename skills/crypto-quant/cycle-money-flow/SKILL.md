---
name: cycle-money-flow
description: "Use when forecasting regime, money-flow, or bubble phase."
version: 1.0.0
author: Ai trading
license: MIT
metadata:
  hermes:
    tags: [cycle, money-flow, investment-clock, regime, forecast, bubble]
    related_skills: [crypto-hold-research, crypto-radar, risk-guard, perp-funding-basis]
---

# Cycle, Bubble & Money-Flow Desk Rules

## When to Use

- User asks dự báo / regime / chu kỳ / dòng tiền / bong bóng / Investment Clock.
- User pastes or references a cycle/money-flow handbook for the desk to internalize.
- Capital-plan or hold research needs a macro+crypto stage overlay before sizing.

Skip pure short-term scalp entries with no regime question — use `crypto-radar` only.

Source ingested (framework, not live oracle): user paste *Cẩm nang chu kỳ kinh tế, bong bóng tài sản & quy luật dịch chuyển dòng tiền (2025–2026)* — synthesis of SonyKieu/Spiderum cycle talk + Investment Clock + 2025–2026 notes. Origin link in paste: `https://www.youtube.com/watch?v=72qIP-r6t3Q`.

**Standing law:** handbook = **regime lens**. Live forecast = lens **+** same-session `crypto-radar`/APIs. Never print handbook prices/rates/“now” as current truth without fetch. Tag handbook-only claims; cite live metrics.

## Four macro phases

| # | Phase | Flow bias | Posture |
|--:|-------|-----------|--------|
| 1 | Recovery | Cash/gold → bonds → stocks/crypto | Early risk-on, cuts |
| 2 | Expansion | Stocks → RE / real economy | Broad risk-on |
| 3 | Overheat | Spec risk → commodities/gold | CB tighten path |
| 4 | Bust | Risk assets → cash | Delever; cash king |

Stocks/crypto move first; RE last.

Loop: cash → bonds → stocks & crypto → commodities & RE → gold/cash.

## Bubble sequence

Displacement → Boom → Euphoria (+leverage, “this time different”) → Panic/burst.

Desk lessons: don’t fight liquidity/Fed; fear “this time different”; no late-cycle leverage; cash is a position; survive via allocation.

## Crypto internal ladder

1. Fiat → stables + **BTC** (BTC.D up)
2. BTC → top L1 (ETH/SOL/BNB)
3. Majors → narratives (RWA/AI/real-yield DeFi)
4. Meme euphoria → stables

Strategic crypto sleeve default in accumulation: **60–70% BTC+top L1**, selective real-revenue alts, **spot DCA**, no futures on hold capital.

## Three ignition switches (observe, don’t assume)

1. Macro liquidity turn: cooling inflation + sustained cuts + M2 up; watch DXY↓, US10Y↓ via live sources.
2. Crypto dry powder: stablecoin mcap multi-week highs + spot ETF net inflows persistent.
3. Time/psychology: long base after prior euphoria; retail fatigue ≠ automatic bottom alone.

0 on → range/accumulation base. 1 on → raise watch. 2+ on + structure → larger risk-on inside capital-plan caps only.

## Handbook 2025–2026 working hypothesis (testable)

- Macro: late-2 → early-3, **higher-for-longer**, selective growth — not free-money melt-up.
- Crypto: post-euphoria **re-accumulation**; high BTC.D; **no blanket alt season**; unlocks hurt weak alts.
- Paste BTC accumulation narrative band ~**60–65k** after 2025 peak — scenario only; overwrite with live structure.
- VN rates/stock/RE/gold lines in paste = paste claims; re-verify before non-crypto advice.

## Forecast output contract

1. As-of time + live F&G, BTC.D, majors price/1D trend.
2. One-line regime: macro phase + crypto stage + falsifiers.
3. Base/Bull/Bear (1–4w tactical; longer only if asked). No single guaranteed target.
4. Switchboard on/off/unknown + missing data.
5. Map to desk capital rules (cash reserve, BTC→ETH, fail-closed alts, no lev).
6. Conditional research view; handbook ≠ proof; gaps through stops possible.

## Anti-patterns

- Extreme Fear alone ≠ bottom.
- Alt season call while BTC.D high + majors 1D bearish without stage-2 evidence.
- Handbook % overriding user’s locked plan caps.
- Inventing Fed/M2/ETF/stablecoin figures.

## Related

`crypto-hold-research`, `crypto-radar`, `risk-guard`, `perp-funding-basis`.

Integrated desk pack (profile local): `~/.hermes/profiles/ai-trading/workspace/investment-desk/` — MASTER.md + desk.json fuse cycle lens, 10-coin watchlist, 500tr conditional plan, risk caps. Public snapshot: https://crypto-500m-plan-preview.vercel.app . Regime labels require measured switches; UNKNOWN macro/ETF cannot become risk-on.
