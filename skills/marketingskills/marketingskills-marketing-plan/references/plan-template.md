# Plan Templates — Strategy and Execution Upgrades

Select the output shape before drafting. Use the default 13-section strategy template below when the user has not supplied one. A supplied outline takes precedence; retain its headings, required tables and checklist format rather than adding a competing structure.

The Quietude plan in `references/example-quietude.md` illustrates the default strategy format, not proof of another client's outcomes.

After a verified six-part WBS already ships and the user asks only to upgrade feasibility/ops, switch to **operator-pack mode** (`references/operator-pack.md`) instead of re-running execution-upgrade from a blank slate.

## Execution-upgrade mode: six parts and six workstreams

Use this mode when the user supplies an audit-to-execution brief with six parts. Apply it to the existing canonical plan; blank example inputs in the attachment do not erase confirmed context.

### Procedure

1. **Extract the output contract.** Map each requested section, table, quantity and decision rule to an acceptance row: requirement, evidence needed, location in the deliverable, status. Read the current plan and latest scope correction before interpreting the template's generic examples.
2. **Audit the current plan.** Keep supported strengths; identify gaps in funnel handoffs, measurable outcomes, task instructions, capacity, cost and ownership. Distinguish a missing business fact from a planning defect; neither warrants an invented score, customer quote or benchmark.
3. **Fix shared definitions before parallel drafting.** Give every specialist the same scope, period, contact definition, creative/asset/placement units, setup-versus-recurring capacity, budget ceiling and base/conditional/parked choices. Use `references/budget-planning.md` for the financial model.
4. **Write one self-contained master.** Populate the six parts below, with the WBS carrying the operational detail. Preserve marketing-only scope through conditional sections rather than omitting required headings or activating unrelated commercial work.
5. **Export the working task table.** Use the same IDs and values in Markdown and CSV. Include what, how, quantity/unit, tools, responsible/accountable roles, dependency, due window, acceptance evidence, metric, cost code and activation status. Keep tasks unchecked until execution evidence exists; choose task count by work required, not table symmetry.
6. **Run acceptance checks.** Parse heading/workstream coverage, required fields, checklist/CSV IDs, duplicate or unresolved dependencies, cycles and requested day coverage. Parse every scheduled row's dates as numbers and require `1 <= start_day <= end_day <= horizon`; report offending IDs and values before declaring the document ready. Review prerequisite timing separately from graph acyclicity: an ongoing review ending at the horizon must not block its own earlier inputs through a false finish-to-start edge. Compute budgets, percentage denominators and scenario formulas in code. When a defect is found, correct the canonical schedule/generator, regenerate derived Markdown/CSV/web fields and delivery mirrors, then refresh acceptance hashes; a display-only patch leaves contradictory handoffs.
7. **Deliver the complete artifact.** Use a full Markdown file with a concise decision summary when that is the established delivery preference. If the user explicitly requests a choice between one long response and multiple parts, ask once; an unanswered format question does not supersede a previously chosen file format or authorize external actions.
8. **Assemble large plans mechanically.** Compute budgets and scenario tables with a local script first. Generate the full task CSV from structured data. Write the prose as section-sized files, join them, then run coverage checks for the six parts, six workstreams, checklist/CSV IDs, dependency graph, budget totals and labeled scenario outputs. Keep this assembly path under parent control when a drafting subagent times out or stalls.

### Required six-part coverage

| Part | Required content and acceptance |
|---|---|
| 1. Audit and gaps | Supported strengths, specific gaps with their consequences, and the change that fixes each gap. |
| 2. Strategy and quantitative goals | Goal tree, ICP/journey hypotheses, pain/objection evidence, proposed positioning and TOFU/MOFU/BOFU/retention message roles. Label untested insights and messaging as hypotheses; keep business outcomes dependent on actual price, margin and sales data. |
| 3. Full-funnel channel architecture | Paid/Owned/Earned/Shared matrix with role, format, cadence, priority, budget denominator/share, output KPI and activation condition. Separate controllable output targets from unknown audience response. |
| 4. Detailed WBS | All six workstreams below, each with assignable tasks, quantities, tools, ownership, timeline, metrics and acceptance evidence. |
| 5. Timeline, RACI and budget | Weekly milestones over the full horizon; one accountable role per workstream; role output targets; setup and recurring budgets; category and channel cost views; three scenarios when requested. |
| 6. Measurement and risk | Daily/weekly/monthly review rules, metric definitions and source/window, operational stop conditions, plus the requested risk table with trigger, immediate action, owner and recovery evidence. |

### Required WBS workstreams

| Workstream | Detail to supply | Scope and evidence check |
|---|---|---|
| 1. Infrastructure, source material and measurement | Brand/KV/templates/FAQ inventory; landing, form and confirmation/error/withdrawal paths; CRM access/dedupe/suppression; UTM/event dictionary; analytics and dashboard acceptance tests. | Allocate setup hours and cash. Distinguish form submission from verified opt-in. Make advertising pixels/CAPI conditional on the actual advertising and consent design; listing a tool is not installation evidence. |
| 2. Content and creative production | Pillar allocation, creative inventory, evidence-bound angle briefs, channel adaptations, sample weekly calendar and AI/human workflow. | State whether percentages apply to ideas, production slots or placements. Include source, editing, review, approval and distribution labor. A multi-image post is one placement; cross-posting a master does not create extra original videos. |
| 3. Paid media and performance | Testing/scaling architecture; cold/warm/hot audience logic; ordered experiments; cash caps and explicit diagnostic, stop and scale rules. | For an organic base, retain zero paid spend and label this a future option. Identify the approved reallocation or extra funding required. State minimum observation/verification windows and evidence thresholds; a CPL cap alone does not prove profitable CAC or statistical significance. |
| 4. Owned channels, SEO and community | Account/profile/pinned-content checklist; candidate keyword clusters and page inventory; on-page/internal-link tasks; community qualification and discussion plan. | Keep search volumes and actual group URLs unknown until researched. Budget articles and moderation. Do not turn topic candidates into verified demand, permission to post or fabricated grassroots support. |
| 5. KOL/KOC, PR, affiliate and partners | Candidate tiers and qualification, shortlist/contact/quote/brief/review/publication/readback workflow, usage/disclosure rights and conditional paid amplification or commission terms. | Separate shortlisted, contacted, contracted and published counts. Do not imply free creator output, earned placement guarantees, affiliate terms or advertising permissions. |
| 6. Activation, handoff and CRM | Lead stages based on explicit actions; service hours/SLA; event or livestream capacity; opt-in lifecycle, suppression and feedback to marketing. | Use a sustainable schedule, not an unsupported daily livestream. Keep offers, checkout, discounts and upsells conditional when unconfirmed. Distinguish requested service from marketing; coordinate all marketing touches through one frequency cap and stop rule. |

Keep the six parts complete even when a branch is inactive: supply its design, dependencies and reason for its status rather than fake financial outcomes or a one-line omission. A task register demonstrates an executable design; live readiness still requires the relevant people, permissions and approvals.

---

## Title block

```markdown
# {Client} — Marketing Plan v1

**Prepared by:** {Author / fCMO name}
**For:** {Founders / leadership team}
**Date:** YYYY-MM-DD
**Status:** Draft v1 — for team review
```

---

## Section 1 — Executive summary

**Purpose:** Lift-and-share. A founder should be able to paste this into a board update or investor email without editing.

**Length:** 400–700 words. Tight.

**Structure:**
1. **One-sentence frame.** What does this plan optimize for? Not "more revenue" — something specific to this client at this stage.
2. **Three big bets, ranked by leverage.** Each is a paragraph. Bet = a high-conviction thesis about where the team should focus capital and attention.
3. **What twelve months looks like, plausibly.** Bullet list. The plausible outcome state at end of plan horizon. Investor-readable.
4. **90-day priorities.** Numbered list. The six (give or take) moves that ship in the first quarter.

**Voice notes:**
- Match the client's voice
- Direct, founder-readable, no marketing-speak
- Use names and numbers (specific channels, specific metrics) — not abstractions
- Tradeoffs named explicitly when they matter

---

## Section 2 — Strategic frame

**Purpose:** Distill positioning, ICP, business-model logic, and brand voice into a single page that any team member or new hire can read to orient.

**Length:** 800–1500 words.

**Structure:**

### What {Company} is, in one sentence
Pulled from positioning doc / seed deck / founder language.

### The category we're claiming
Is the company creating a new category, redefining an existing one, or competing in a defined category? Name it. State the category-defining frame in 2–3 sentences. Reference the source (founder's words, ICP doc, etc.).

### Who we're for (ICP, distilled)
Demographics / firmographics + stated problem vs. real problem + what they're actually buying. Tight, 4–6 bullets.

### The business model logic
How does the company make money? What's the customer-acquisition unit economics theory? What's the compounding channel thesis (if any)? Pulled from seed deck / financial model / founder narrative.

### Brand voice (the non-negotiable)
If the client has documented voice rules, list them. YES / NO vocabulary. CTA rules. Tone. Core method (initiatory, explanatory, narrative, etc.). Every other section of the plan must respect these.

**Voice notes:**
- This section is the most "lift from existing materials" — don't invent positioning. Surface what's there.
- If positioning is unclear or contradicted across materials, flag it in Section 13's open decisions.

---

## Section 3 — Current state

**Purpose:** Anchor the plan in reality. What's the team, budget, in-flight work, and stuck work *today*?

**Length:** 1000–2000 words.

**Structure:**

### Team composition (marketing surface area)
Table of every person with marketing surface area:

| Person | Role | Marketing surface area |
|---|---|---|

Be honest about gaps. If there's no dedicated marketing hire yet, name when one becomes necessary and what role (see `references/team-and-agency-model.md` — first hire should be π-shaped strategist titled Manager or Lead, not VP/CMO).

### Marketing budget (current)
- Paid acquisition: $X/mo
- Tooling stack: list with estimated cost
- Retainers / fCMO: list
- Headcount: list
- Blended CAC: $X (must include salaries, content costs, tools, retainers — not just paid spend; see `references/budget-planning.md` for the calculation)
- Current spend as % of ARR: X% (compare against 5–40% range)

State the funding-stage tier this maps to (see `references/funding-stage-unlocks.md`). Implication: what 90-day plan must produce *without* lever pulls that require future budget.

### Phase of SaaS growth
Name the current phase: $0–10K ARR / $10K–100K / $100K–1M / $1M–$10M / $10M+. Each phase has its own binding constraint and dominant growth pattern (see `references/growth-patterns.md`). Section 10 sequences the move into the next phase.

### What's already done (acknowledge, then build on)
Table:

| Asset | Status | Marketing leverage |
|---|---|---|

This is where past launches, PR moments, content pillars, certifications, notable users get acknowledged. **Critical**: don't write a plan that ignores work the team is proud of.

### What's in-flight (drafted but not shipped)
Table:

| Item | Status | Blocker |
|---|---|---|

Be honest about blockers. Where the blocker is "no time" or "no decision," that goes to Section 13's open decisions.

### What's stuck (and needs to unstick this quarter)
Table:

| Issue | Cost of inaction | Action |
|---|---|---|

Stuck things are the most leverage-positive places to focus the first weeks of the 90-day plan.

### Audit rubric snapshot
17-section scored snapshot using the embedded current-state rubric. See `references/current-state-rubric.md` for the full rubric and scoring guides.

If a prior scored audit exists, retain its source and assessment context. Otherwise note "scored from materials" and assess only supported conditions. Use `UNKNOWN`, `NOT_ASSESSED` and `N/A` instead of inventing numeric scores; include evidence or the evidence needed in the Note column.

| # | Section | Score | Note |
|---|---|---|---|
| 1 | Positioning | 0–5 | |
| 2 | Customer research | 0–5 | |
| ... | ... | ... | ... |
| 17 | Internationalization | 0–5 | |

**Complete numeric audit only:** Total X / 85 (Y%). **Incomplete audit:** show assessment coverage and unassessed rows; omit a complete-audit total/percentage. Interpret only evidence-backed strengths and gaps.

**Voice notes:**
- Honest > polished. If the client's metrics are bad, name them. Founders read past sugar-coating.

---

## Section 4 — Acquisition

**Purpose:** Answer "how do strangers become aware of us?" Map every channel: current state, planned moves, skipped (with reason).

**Length:** 1000–1800 words.

**Structure:**

### Current state
Brief. What's working today, what's not, what the data shows about channel mix.

### The plan
Numbered "Moves." Each move is a paragraph (3–6 sentences) describing the channel, the thesis, and the specific work. Common moves:

- **Move 1 — SEO (and content)** — Reference the SEO plan if one exists (`seo/plan.md`). Otherwise: keyword research, pillar/spoke structure, content cadence.
- **Move 2 — App Store / Play Store optimization** (for consumer apps) — Listing rewrite, screenshot tests, ASO keyword targeting.
- **Move 3 — Founder-led channels** — LinkedIn for B2B/SaaS, Twitter/X for tech, Instagram for consumer. Cadence, topics, owners.
- **Move 4 — PR amplification** — What's the credibility anchor? How to amplify it.
- **Move 5 — Events (if applicable)** — Live events, conferences, webinars. Acquisition vs. activation role.
- **Move 6 — Hardware / commerce surface (if applicable)** — Shopify storefront, Amazon, retail.
- **Move 7 — B2B sales support** — Case studies, partner pages, vertical-specific content.
- **Move 8 — Paid layer (when budget unlocks)** — Apple Search Ads, Meta, LinkedIn, Google. Held until specified funding stage.

### 90-day acquisition moves
Week-by-week breakdown of the ships in the first quarter.

### 12-month acquisition outlook
Quarter-by-quarter outcome state (Q1 / Q2 / Q3 / Q4).

### Skills + tools
- **Skills:** list relevant marketing-skills repo skills (`seo-audit`, `ai-seo`, `ads`, `social`, `competitors`, etc.)
- **MCPs / APIs:** list connections (Ahrefs API, GA4 MCP, Typefully MCP, Stripe MCP for LTV math, etc.)

---

## Section 5 — Activation

**Purpose:** Answer "once someone tries us, do they have an experience that converts?"

**Length:** 800–1500 words.

**Structure:** Same as Acquisition (Current state / The plan / 90-day / 12-month / Skills + tools).

**Common moves:**
- Bedrock fixes (broken signup, broken onboarding gates, etc.)
- Onboarding tests / rebuild (often the most leveraged move at this stage)
- App Store listing rewrite (cross-references to Acquisition)
- Lifecycle Flow ship order (when to ship onboarding emails vs. hold for product stability)
- Paywall + pricing review (often Activation × Revenue)

### Skills + tools
`onboarding`, `signup`, `paywalls`, `copywriting`, `marketing-website-design`, `ab-testing`, etc.

---

## Section 6 — Retention

**Purpose:** Answer "once someone converts, do they stay and deepen?"

**Length:** 800–1500 words.

**Structure:** Same as above.

**Common moves:**
- Lifecycle email flows (post-purchase, lapsed user, win-back)
- Subscription / preference centers
- Churn reconciliation (often metric definitions don't match across surfaces)
- Hardware → software activation paths (for hybrid businesses)
- Annual plan default tests (cross-references to Revenue)

### Skills + tools
`emails`, `churn-prevention`, `copywriting`, `paywalls`, etc.

---

## Section 7 — Referral

**Purpose:** Answer "do retained users bring more users, and at what cost?"

**Length:** 500–1200 words.

**Structure:** Same as above.

**Common moves:**
- Ambassador / affiliate program launch (if inbound interest exists, lead with it)
- Share-after-value moments built into product
- Founder amplification (founder as referrer-zero)
- Long-game expert / Guides / certified-host network
- Gifting flows (for consumer / hardware)

### Skills + tools
`referrals`, `social`, `emails` (for ambassador lifecycle), `copywriting`, etc.

---

## Section 8 — Revenue

**Purpose:** Answer "what do we charge, who pays, and how does it compound?"

**Length:** 500–1200 words.

**Structure:** Same as above.

**Common moves:**
- Pricing audit (what's actually charged today vs. listed?)
- Annual plan default tests
- Hardware → software bundling formalization (for hybrid businesses)
- Storefront / commerce page optimization
- B2B case studies + sales material
- Long-term value pools (data licensing, enterprise expansion) — flagged not executed in 12-month plan

### Unit economics
Required table:

| Metric | Value | Note |
|---|---|---|
| ARPC (avg monthly revenue per customer) | $X | Pulled from Stripe / billing |
| Blended CAC | $X | Includes all marketing costs, not just paid |
| Annual retention rate | X% | 1 − annual churn |
| LTV (rough) | $X | ARPC × 12 / annual churn |
| LTV / CAC | X | Health benchmark: > 3 |

These feed the budget math in Section 10. If any of these are unknown, flag in Section 13 as top open decision.

### Skills + tools
`pricing`, `paywalls`, `sales-enablement`, `revops`, `ab-testing`, etc.

---

## Section 9 — 90-day roadmap

**Purpose:** The tactical execution layer. Every move ships within a named week, with an owner.

**Length:** Tables, not prose. Should fit on one printed page if possible.

**Structure:** Give each row an ID, proposed owner, start/end day, prerequisite, deliverable, metric and acceptance evidence. Define phase boundaries across the entire requested horizon; for 90 days, include the final partial week after week 12. Parse the dates and dependencies instead of assuming weekly labels cover every day.

### Days 1–14 — Unblock
Highest-confidence, lowest-cost discovery and correction work; establish actual owners and scope.

| ID | Days | Move | Stage | Role | Prerequisite | Acceptance evidence |
|---|---|---|---|---|---|---|

### Days 15–28 — Foundation
Build the costed source, capture and measurement foundation; prepare the first package within the chosen capacity ceiling.

### Days 29–56 — Repeat
Test the authorized first destination, read back the result and repeat only as measured production/review capacity permits. Delay dependent work when prerequisites slip.

### Days 57–90 — Learn and choose
Review mature cohorts, improve the demonstrated bottleneck and decide whether to fund another channel or production cycle. Include days 85–90 explicitly; do not turn a 28-day capacity model into an unbudgeted 90-day output promise.

---

## Section 10 — 12-month outlook

**Purpose:** Quarterly milestones with explicit funding-stage capability unlocks named, anchored against a defensible growth pattern.

**Length:** Four sub-sections, one per quarter. ~250–400 words each. Plus a short framing paragraph at the top naming the budget method and growth pattern.

### Framing (top of Section 10)

State explicitly:
- **Budget method used.** Revenue-Based or Goal-Based when supported; otherwise a capped learning budget with unknown economics. See `references/budget-planning.md`; show actual arithmetic and assumption labels.
- **Budget horizon and total.** Do not annualize a monthly option as a commitment. Include any experiment reserve within the user's hard ceiling, or identify an unapproved increase separately.
- **End-of-year commercial outcome.** Use evidence-backed goals where possible; when inputs are missing, state milestone conditions and keep ARR/LTV/payback unknown rather than inventing a forecast.
- **Growth pattern expected.** Linear (predictable $X MRR added per month), step-function (plateau between deliberate jumps), or layered S-curves. For VC-backed Series A+, anchor against 3-3-2-2-2 and show whether the plan matches it or explicitly chooses a different trajectory. See `references/growth-patterns.md`.

### Structure (per quarter)

#### Q{N} — Months {X}–{Y}

**Funding state:** {tier} per `funding-stage-unlocks.md`

**Focus:** One-sentence focus theme for the quarter.

**Outcomes by end of Q{N}:**
- Bulleted outcome list (5–8 items)

**KPI targets:** 3–5 specific numerical targets.

**Channel/Product/Market S-curve position:** Which curves are growing, which are plateauing, which is the next one being staged for this quarter (see `growth-patterns.md` — layering principle).

---

## Section 11 — Marketing operations stack

**Purpose:** The fCMO differentiator. Show how a small team + agentic tooling executes the plan without hiring at every channel.

**Length:** Tables + brief explanation.

**Structure:**

### The thesis
Map each stage to its actual or proposed operator, tool, output, review capacity and hours. Describe where AI assists and where a person supplies source material, validates, approves or publishes. Installed tools and agent counts do not establish headcount replacement or throughput.

### Skills mapped to AARRR stages

| Stage | Primary skills | Supporting skills |
|---|---|---|
| Acquisition | (list) | (list) |
| Activation | (list) | (list) |
| Retention | (list) | (list) |
| Referral | (list) | (list) |
| Revenue | (list) | (list) |
| Cross-cutting | (list) | (list) |

### MCPs / APIs mapped to stages

| Stage | Existing connections | fCMO tooling layer |
|---|---|---|

### A concrete example
Use a real execution receipt when available and state what it demonstrates. If the workflow has not run, show a labeled proposed walkthrough with its required inputs, outputs and acceptance test; do not invent an operational event to prove the stack.

### Capability unlocks by funding stage

| Stage | Headcount | Tooling | Channels live |
|---|---|---|---|
| (current) | (list) | (list) | (list) |
| (next round) | (delta) | (delta) | (delta) |
| ... | ... | ... | ... |

### Team and agency model (RACI)

Apply the principle from `references/team-and-agency-model.md`: strategy in-house, execution often outsourced.

| Function | Owned by (internal strategic role) | Executed by (IC / contractor / agency) |
|---|---|---|
| Growth marketing (demand engine) | | |
| Product marketing (story engine) | | |
| Content marketing (trust engine) | | |

If the team is missing a strategic owner for one of these functions, the first 90-day move (Section 9) should be the hire — Manager or Lead title, π-shaped if possible, not VP/CMO.

If execution capacity is the gap, name the contractor or small niche agency in the right cell rather than the team's existing IC.

Pull from `references/funding-stage-unlocks.md`.

---

## Section 12 — Tactical idea bank

**Purpose:** Select the tactics that fit this client's objective, scope, budget and capacity, tagged by AARRR and priority. Produce an exhaustive library cross-reference only when explicitly requested.

**Length:** A decision-ready shortlist; extra rows must add a distinct executable choice, not demonstrate library coverage.

**Structure:**

### Intro paragraph
Explain the cross-reference: Sections 4–8 prescribe what's *being done*. This section maps what's *possible*.

### Status legend

- **Now (Q1)** — already in 90-day plan
- **Q2** — post-foundation layer-in
- **Q3+** — post-seed-close or post-GA expansion
- **Q4+** — long-game
- **Skip / off-brand** — incompatible with brand voice or business model

### 12.1 Acquisition ideas

By status (Now / Q2 / Q3+ / Q4+ / Skip), tables of relevant marketing-ideas by number.

| # | Idea | Client note |
|---|---|---|

### 12.2 Activation ideas
### 12.3 Retention ideas
### 12.4 Referral ideas
### 12.5 Revenue ideas
### 12.6 Cross-cutting / brand foundation ideas

### Idea-bank summary
- Show the selected Now / Later / Skip choices and explain material exclusions.
- Tie each Now tactic to an owner, work item, resource allocation and stop criterion.
- Treat tactic counts as inventory, not effectiveness or market-stage evidence; omit an arbitrary library-coverage percentage.

Use `references/idea-cross-reference.md` for a requested exhaustive audit. Otherwise apply scope, audience, brand, budget and capacity filters to the shortlist.

---

## Section 13 — Measurement, RACI, open decisions, appendix

**Purpose:** Operational close. Define how the plan gets measured, who owns what, what's still TBD, and where to find the deeper docs.

**Structure:**

### Measurement — the metrics that matter

**North star (proposed):** One metric that captures the business-model thesis. For Quietude it was blended-LTV-to-blended-CAC; for a B2B SaaS it might be NRR × NPS; for a marketplace, take-rate × monthly transacting users. Make it specific to the company.

**Leading indicators by AARRR stage:** Table:

| Stage | Leading indicators |
|---|---|
| Acquisition | ... |
| Activation | ... |
| Retention | ... |
| Referral | ... |
| Revenue | ... |

**Review cadence:**
- Weekly: who syncs with whom, on what
- Monthly: who reviews what
- Quarterly: plan recalibration trigger

### RACI

| Domain | Responsible | Accountable | Consulted | Informed |
|---|---|---|---|---|

Common domains: strategic plan, brand voice, app/product implementation, lifecycle, SEO content, App Store, founder-led social, events, ambassadors, B2B sales, pricing, investor narrative, future hires.

### Open decisions blocking the plan

Ranked by impact. Each is: name + impact + what's blocked.

1. (highest impact) ...
2. ...
8. (lowest impact) ...

### Appendix — deep-dive links

**Published in this repo / shared with team:** {relative paths to docs in the shared repo}

**Founder-authored strategic context** (internal knowledge base): {names of docs the team has access to outside the plan repo}

**fCMO working drafts** (not yet published): {names + how to access from author}

---

## Closing line

```markdown
*{Client} Marketing Plan v1. Prepared by {Author}, {Date}. For team review and discussion.*
```

---

## Per-section heuristics for "is this section done?"

- **Section 1** — A non-Quietude reader could understand the company's growth thesis from this alone.
- **Section 2** — Brand voice rules are explicit enough that any new copywriter could follow them.
- **Section 3** — All "in-flight" items have an owner and a blocker named.
- **Sections 4–8** — Each move names a skill (`some-skill`) and a tool (Customer.io MCP / Stripe MCP / Ahrefs / etc.).
- **Section 9** — Every row has an owner.
- **Section 10** — Each quarter names the funding stage explicitly.
- **Section 11** — At least one concrete operational example proves the stack thesis.
- **Section 12** — Skip list has rationale, not just absence.
- **Section 13** — North-star is specific to this company (not generic "ARR growth").
