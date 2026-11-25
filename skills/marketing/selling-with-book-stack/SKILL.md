---
name: selling-with-book-stack
description: "Use when explicitly asked to sell or monetize."
version: 1.0.0
author: agent-00-orchestrator
license: MIT
metadata:
  hermes:
    tags: [sales, offer, funnel, hormozi, brunson, leads, money-model, ecommerce, crm]
    related_skills: []
---

# Selling With Book Stack

## Overview

This is an on-demand reference skill, NOT permanent context. Use the 7-document sales library only for the sales portion of the current request. Never treat the library as general brand memory or automatically pass it to other agents. Its contents do not carry authority over unrelated work or future sessions.

Run the sales library and its optional GitHub tooling only when the activation conditions below are met. Match the requested sales deliverable; do not force the entire S0–S7 pipeline onto a narrow question.

**Core principle:** Market → Offer → Money model → Leads → Close → Funnel pages → Scale. Tools serve model.

**Knowledge base:** `/Users/buithiphuongthao/Desktop/nghiên cứu/THONG-KE-KIEN-THUC-7-TAI-LIEU.md`

**Books:** $100M Offers, $100M Leads, $100M Money Models (Hormozi); Network Marketing Secrets (Brunson); ProCode (Worre); 210 power words; Sổ tay 100.

Address **Anh Huy**. Match user language (default Vietnamese).

## When to Use

Activate only when the current user request explicitly asks for selling, sales offer packaging, sales pricing, monetization, sales conversion, closing, or applying this sales library. Merely owning a product, requesting marketing, research, launch, content, design, automation, or saying 'use all skills' does not qualify.

Do not load the knowledge-base file until activation is established. Do not load sales references into research, free-reach marketing, product analysis, design, or other agents. For mixed work, isolate sales knowledge to the sales subtask.

When the user requests free/no-sell work, do not use this skill or its references. Use the relevant non-sales skills independently; do not route the work through this skill's free-reach mode. A later session or unrelated request starts inactive, even if an earlier task involved sales.

If the current monetization path is wagering, cash-out or other real-value stake/reward mechanics, stop sales packaging for that path and hand the work back to non-promotional compliance or a non-wagering redesign under `marketing-plan`. Do not keep promoting deposit, stake or cash-out conversion under entertainment wording. When price remains undecided, keep SKU/price fields TBD and do not carry earlier illustrative prices forward as selected offers.

**When NOT to use:** research, non-sales marketing, free user acquisition, community growth, launch without a sales objective, UI/web design, unrelated agent coordination, content without sales intent, code debugging, illegal spam, fabricated guarantees.

**Capital → target cash** ("vốn X, kiếm về Y", turn seed cash into a higher cash total, personal runway monetization) **does activate** this skill: it is an explicit monetization ask. Run the compressed pack plus `references/capital-to-cash-playbook.md`. Never frame the output as guaranteed profit, passive investment yield, or market-validated demand without paid evidence.

### Task-scoped activation and deactivation

- If the current task has no explicit sales objective, leave this skill and its source library inactive. Choose non-sales skills from the user's actual objective; do not prescribe game metrics, budgets, tools, or CTAs here.
- If a sales task changes to free/no-sell work, stop the sales workflow. Treat earlier sales artifacts as inactive for that task; do not edit, delete, publish, or propagate them without authorization.
- A follow-up continuing the same sales task may use the relevant sales references. A different task or new session has no inherited sales activation; assess its own request.
- Inspecting or editing this skill at the user's request is maintenance, not permission to apply its sales frameworks or read its source library.

| Current request | Sales library |
|---|---|
| Research a market, design a website, coordinate agents | Inactive |
| Grow a free product or community, even with paid promotion | Inactive |
| Use all relevant skills, without a sales objective | Inactive |
| Package an offer, build a sales funnel, improve closing | Active for that sales scope only |
| Research first and separately build a sales offer | Isolate the sales references to the offer subtask |
| Start a new session about a different subject | Inactive |

---

## Best-fit GitHub stack

Fit = **funnel + money path + CRM**. Not giant catalog shop unless multi-SKU retail.

| Priority | Repo | Maps books |
|---|---|---|
| **#1 Funnel** | https://github.com/autonnel/autonnel | LP→checkout→bump→one-click upsell→TY = Money Models + Brunson + Offers. Stripe/PayPal, Shopify/Woo/Picocart, ad postbacks, MCP. Apache-2.0 |
| **#1b Skills** | https://github.com/autonnel/autonnel-skills | blueprint, upsell-flow, CRO audit, platform-picker, self-host launch, CAPI tracking |
| **#2 CRM** | https://github.com/twentyhq/twenty | Engaged leads, follow-up (ProCode PC7), Core Four tasks |
| **#2b ERP** | https://github.com/Dolibarr/dolibarr | Invoice/order/stock + simple CRM |
| **#3 Commerce** | medusajs/medusa · saleor/saleor · bagisto/bagisto · woocommerce/woocommerce · spree/spree | Multi-SKU when Autonnel alone insufficient |
| **#4 Lists** | finsilabs/awesome-ecommerce-skills · jluterek/awesome-ecommerce | CRO/CLV checklists only |

### Default matrix

| Product type | Stack |
|---|---|
| Info/course/challenge/coaching ≲$500 | Autonnel + Stripe + email + Twenty |
| Service/high-ticket ≳$500 | Landing+form→booking; Twenty pipeline; ProCode close |
| Physical/many SKUs sold by the user | Medusa/Bagisto/Woo + Autonnel post-purchase |
| Affiliate publisher | Verified affiliate links + the existing distribution channel + commission reconciliation; merchant checkout remains external |
| NM/team duplicate | Brunson 3 funnels on Autonnel; ProCode in Twenty; no income claims |
| Personal brand → sell | Sổ tay Ai/Ở đâu/Mồi + Leads content + Autonnel |

Do **not** default Magento unless enterprise already in place.

See also `references/github-stack.md`.

---

## Mandatory pipeline S0→S7

```text
S0 Intake brief
S1 Market (Offers + Sổ tay)
S2 Grand Slam Offer (Offers)
S3 Money Model (Money Models)
S4 Lead system (Leads + power-word hooks)
S5 Conversation/Close (ProCode + Brunson Epiphany if story-led)
S6 Funnel blueprint + tool wiring
S7 Scale (lead getters + duplication) + metrics
```

Checklists: `references/stage-checklists.md`. Brief: `references/product-brief-template.md`.

### S0 Intake

Fill product brief. Min: what sold, monetization/fulfillment role, dream outcome, avatar+where, price band, assets and goal with its period. For Anh Huy, present a compact selectable brief first, preserve submitted answers and follow up only on unresolved dependencies. Label nonblocking defaults `GIẢ ĐỊNH`; keep the user's budget currency, period and strict bounds intact.

**Payer ≠ player:** when one person pays and another uses (e.g. parent buys, child plays), capture **two layers** in the brief but keep **one primary message per funnel**. Ads/content speak to the payer's pain; product loops (share, rank, challenge) speak to the player. Never mash both into one creative.

**Intake blockers before full pack:** stage (idea/MVP/live), product category or primary SKU, primary avatar, monetization/fulfillment role, budget band with period and available distribution channel. Batch independent decisions, then ask only dependencies their answers create. If the request is to recommend products or sources, leave SKU/program selections null and compare candidates; an unchosen SKU is not a reason to withhold the requested proposed plan. Record platform groups as distribution access, not automatically owned contacts or messaging consent.

**Affiliate-publisher branch:** adapt S2–S7 to the publisher's control before recommending tools. Define the merchant offer accurately, substantiate recommendation claims and use the program's attributable purchase path; do not promise merchant prices, returns, stock or guarantees on the publisher's behalf. Keep GMV separate from expected, approved and paid commissions, and use commission contribution, cash timing and work capacity for scale decisions. Check current official eligibility, external-traffic rules, attribution, caps, validation and payout terms before treating a program as usable. Keep unknown terms explicit. For topical depth, load the **Affiliate Publisher / Content-led Commerce** archetype from the `marketing-plan` skill's linked client-types reference through `skill_view`. That workflow replaces merchant-specific inventory, owned-checkout and upsell assumptions for this branch.

### S1 Market

- Score: Pain · Money · Targetable · Growing
- Starving crowd; niche to charge
- **One avatar** (Brunson product-lover vs builder — one message)
- Out: `MARKET_CARD`

### S2 Grand Slam Offer

1 Dream Outcome → 2 Problems → 3 Solutions → 4 DIY/DWY/DFY → 5 Trim&Stack → 6 scarcity/urgency/bonuses/guarantee (`If not X in Y → Z`) + MAGIC name → 7 Value Equation `(Dream×Likelihood)/(Time×Effort)`

**210 power words** only after offer solid — headline/CTA clusters Giá|Urgency|Trust|Benefit|CTA. Words ≠ offer.

Out: `OFFER_SPEC`

### S3 Money Model

`Attraction → Upsell → Downsell(on no) → Continuity`

- 30-day profit/customer ≥ CAC
- Never same SKU only cheaper after no — change terms or features
- Name concrete subtypes (Win-money-back, Decoy, BXGY, Pay-now-or-later; Classic/Menu/Anchor/Rollover; Seesaw/Penalty/Feature; Bonus/Discount/Waived-fee)
- Greenfield: one layer at a time
- **Cash ledger (required on capital-target work):** compute in code and keep separate — starting capital, unearned deposits, collected earned revenue, direct costs, fixed launch burn, earmarked reserves (tax/fee and warranty/refund placeholders are funds held, not a tax opinion), ending cash after reserves, optional owner-labor accounting. Deposits raise bank cash but are not earned profit until the milestone is delivered. Scenario rows for `0..N` clients; mark full-pay N as best-case, not base, until real close rates exist.
- **Commodity price trap:** if public competitors sell the bare deliverable much cheaper, price the operational bundle (pipeline, scripts, SLA, training) and keep a scope-cut downsell — do not compete as "same page, higher fee".

Out: `MONEY_MODEL_MAP`

### S4 Leads

- Define **engaged lead** action
- LM 7-step if high-ticket/trust gap
- **One** Core Four first + Rule of 100 (warm or content typical for first cash)
- CTA = action + reason now
- More → Better → New
- Twenty stages: New → Engaged → Offer sent → Won/Lost → Continuity; every touch sets next follow-up
- **First-cash guards:** pre-first-sale burn ceiling; total launch ceiling; kill-switch after a stated count of allowed approaches + real conversations with zero paid (revise offer/ICP or stop — do not unlock ads to paper over silence); ads parked until one paid order or an explicit demo threshold; only contact channels the operator is permitted to use (no scrape/spam playbooks).

Out: `LEAD_PLAN`

### S5 Close

- STEPP asset list
- Epiphany Bridge if story-led
- Demo stack + permission CTA
- Big Six objections: listen→relate→story→bridge
- PC8–10 quantity/speed/simplicity
- Ethical only; no fake scarcity

Out: `CLOSE_SCRIPT_OUTLINE`

### S6 Funnel + wiring

| Book idea | Page role |
|---|---|
| Hook/mồi/MAGIC challenge | LANDING |
| Core/tripwire pay | CHECKOUT |
| Upsell/bump | UPSELL |
| Delivery + BAMFAM | THANKYOU |
| Pay fail | ERROR |
| High-ticket apply | LANDING→form→booking + CRM |

**Build order: checkout truth first, landing second.**

Implement path: autonnel-skills patterns → Autonnel deploy when asked → Stripe → catalog if needed → Twenty → server-side conversions when ads live.

Out: `FUNNEL_SPEC` + `TOOL_WIRING`

UI polish skills only **after** offer/funnel spec exists.

### S7 Scale

- Lead getters: self→referral→employee→agency→affiliate
- Metrics: LTGP:CAC, 30-day cash, opt-in%, checkout%, upsell%, refund%
- ProCode 5 pillars if team; Brunson L2/L3 only after L1 converts

Out: `SCOREBOARD` + 14-day experiments (one bottleneck)

---

## Book → tool feature map

| Library | Tool |
|---|---|
| Offers stack/Value Eq | Landing sections + checkout lines + bonuses |
| Scarcity/urgency | Real caps/timers only |
| Guarantee | Policy copy + CRM tag |
| Attraction | Tripwire/decoy dual SKU |
| Upsell | Autonnel UPSELL chain |
| Downsell | Alternate path/feature tier — not silent same-SKU cut |
| Continuity | Subscription + fee/bonus framing |
| Lead magnet | Opt-in + email + Twenty contact |
| Core Four | Twenty tasks; no illegal scrape how-to |
| Paid ads | Server-side postbacks |
| Brunson 3 funnels | Multi-landing paths |
| ProCode follow-up | Next activity required |
| 210 words | Headline/CTA lexicon |
| Sổ tay Why-How-What | Brand story block |

---

## Delivery format (every engagement)

1. Assumptions  
2. MARKET_CARD  
3. OFFER_SPEC  
4. MONEY_MODEL_MAP  
5. LEAD_PLAN  
6. CLOSE_SCRIPT_OUTLINE  
7. FUNNEL_SPEC + TOOL_WIRING  
8. SCOREBOARD + 14-day actions  
9. Open questions (≤5 blockers)  

Optional save: `/Users/buithiphuongthao/Desktop/nghiên cứu/sell-packs/<product-slug>/`

Also mirror strategy artifacts under `~/marketing-plans/<product-slug>/` (`research.md`, `progress.md`, `final_plan.md`) when the engagement is a GTM plan, not only a sell pack.

---

## Hard rules

| Rule | Why |
|---|---|
| Offer before ads creative | Bad offer wastes spend |
| Engaged lead > raw count | Vanity lists |
| Checkout truth before landing hype | Overpromise |
| No fake scarcity/guarantee/income claims | Ethics/law |
| No naked same-SKU discount after no | Trust |
| One avatar one message per funnel | Brunson |
| Rule 100 before "dead market" | Leads |
| Tools optional until S2–S3 clear | Stack tourism |
| LinTech HITL if public via agent-00 | Existing OS |
| No verbatim book dump | Copyright — frameworks only |

### Reject rationalizations

| Excuse | Counter |
|---|---|
| "Chỉ cần landing đẹp" | No OFFER_SPEC = no build |
| "Ads trước" | Need offer + money model + engaged def |
| "Giảm giá cho dễ" | Stack value / feature-or-terms downsell |
| "Full 4 Core Four luôn" | One method × Rule 100 |
| "Repo khác hot hơn" | Matrix fit first |
| "NM hype" | ProCode truth; no tourist tactics |

---

## Common mistakes

- Woo/Bagisto first for single info offer → Autonnel first  
- Power-word spam without Value Equation  
- Continuity-only attraction → cash crunch  
- No downsell path  
- CRM without next follow-up date  
- Three Brunson funnels before one path converts  

---

## Related skills (explicit handoff only)

References are not automatic load instructions. Select another skill only when the current task needs it. Share the brief and the necessary task artifact, not the sales source library or whole sales skill. Do not pass sales context to a non-sales subtask.

- marketing-plan / marketing-council / launch — optional for a sales-related strategy task
- gsheet-control-plane / telegram-hitl-gate — only for applicable LinTech content gates
- opa-knowledge — only for Huy/OPA claims in the current task

## Supporting files

- `references/product-brief-template.md`
- `references/github-stack.md`
- `references/stage-checklists.md`
- `references/capital-to-cash-playbook.md` — vốn X → mục tiêu tiền Y: assumptions, path choice, coded cash scenarios, stop-loss, local deliverables
- `references/free-reach-mode.md` — retired redirect only; no-sell work belongs outside this sales skill.

## Smoke example

User: "Bán khóa 6 tuần giảm mỡ 1.997.000đ" → S0–S7 full pack; tripwire→core→upsell→membership; warm+content Rule 100; Autonnel+Twenty; no ads day-one without checkout truth.

User: "vốn 10 triệu, kiếm về 20 triệu" → activate capital-to-cash playbook; productized service vs broker vs digital-product tree; coded 0..N cash table; public commodity price anchor; offer pack + stop-loss; local plan folder; no guaranteed return language; no spend/contact/public without order.
