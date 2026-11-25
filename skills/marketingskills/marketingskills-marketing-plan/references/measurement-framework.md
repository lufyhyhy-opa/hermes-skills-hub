# Measurement Framework — KPIs, North Stars, Cadence

Every plan needs a measurement section that tells the team how to know if the plan is working. This doc is the source for Section 13's measurement subsection.

**Related docs:**
- `growth-patterns.md` — the 3-3-2-2-2 VC growth path (3× in years 1–2, 2× in years 3–7 from $1M ARR) and which phase of SaaS growth the company is in ($0–10K / $10K–100K / $100K–1M+)
- `budget-planning.md` — CAC calculation (blended, not paid-only) and the forecasting reality check (forecasts under $100M ARR are educated guesses, not precise predictions)

## The north-star principle

A north star is one metric that captures the business-model thesis at the highest level. It should:
- Be derivable from the funnel + revenue model
- Move slowly enough to be a strategic compass (not whipsawed by weekly noise)
- Trade off correctly against other metrics — improving the north star should generally improve the business

Don't default to "ARR" or "MRR" alone. Those are outcomes, not norths. Pick something that captures the business model.

## North-star patterns by business model

### B2B SaaS (subscription)
- **Net Revenue Retention (NRR)** — keeps existing customers + expansion in focus
- Alternative: "Logo retention × expansion ARR"
- Why: ARR alone hides churn / lets gross-add growth mask product fit problems

### D2C consumer app (subscription)
- **Blended LTV / blended CAC** — keeps unit economics honest as paid layer scales
- Alternative: "Day-35 paid users from cohort × LTV"
- Why: monthly subscription metrics are volatile; cohort × LTV smooths it

### Hybrid hardware + software (e.g., Quietude)
- **Blended LTV / blended CAC across hardware + software** — captures the wedge thesis
- Alternative: "Hardware-buyers-to-subscriber conversion × blended margin"
- Why: hardware revenue isn't free (cost to make); subscription revenue isn't expensive to acquire if hardware funds it

### Marketplace (two-sided)
- **Liquidity ratio × take-rate** — captures both sides + monetization
- Alternative: "Monthly transacting users × take-rate × repeat frequency"
- Why: GMV alone doesn't capture whether the marketplace is becoming a habit

### Developer tool / open source
- **Weekly active developers × paid-conversion** — captures both adoption and monetization
- Alternative: "Weekly active orgs × seats per org × ARPU"

### Content / media business
- **Daily active readers / listeners × ad revenue per session** — captures both reach and monetization
- Alternative: "Subscriber count × retention × ARPU"

### Commerce (DTC, non-subscription)
- **Repeat purchase rate × AOV × frequency** — captures monetization layered on quality of customer
- Alternative: "Customer LTV / CAC × payback period"

## Marketing-only contact acquisition

Apply this procedure when the assignment is multichannel marketing and voluntary contact growth; preserve the separate business North Star rather than importing revenue requirements into the marketing scoreboard.

1. Separate four layers: platform-reported reach/views, measurable site visitors, rented community membership and permissioned first-party contacts. Keep reach per platform because platform totals cannot establish unique cross-platform people.
2. Define the marketing North Star as new unique valid opted-in contacts per reporting week. Specify timezone, week boundary, cutoff and the first time a contact qualifies. Require an appropriate verified/reachable contact method, purpose-specific consent evidence, applicable audience eligibility and active permission at cutoff. Re-check reachability and suppression at cutoff: known_unreachable, hard-bounce, withdrawn consent or policy suppression exclude the contact from the North Star and keep a diagnostic reason bucket; one successful verification earlier does not prove reachability forever, and do not send probe messages just to manufacture a KPI. Exclude duplicates, pending verification, invalid records and withdrawn permission; retain their counts as diagnostics.
3. Design the capture path around a real benefit: relevant guidance, an actual schedule or a real community activity. Ask for one suitable contact method, preserve an optional demo/skip path when that is the chosen funnel, and separate marketing consent from analytics consent. Group membership supplies neither a contact export right nor permission to DM.
4. Store an opaque contact ID, protected contact method, consent purpose/version/time/proof, first and last known source, content reference, engagement state, suppression state and responsible owner. Keep raw contact information out of public Sheets, URLs, logs and drafting prompts; the reporting view should be aggregated or de-identified.
5. Report contact validity/duplicates/withdrawals alongside volume. Define the downstream meaningful action from the actual product, then read activation and return only for cohorts whose observation windows have closed. Keep the full closed qualification cohort as the Activation-7d denominator; do not drop non-returners to improve the rate. Track coverage = contacts with valid observation / closed cohort; when coverage is incomplete, mark the whole-cohort activation rate `NOT_MEASURABLE` and, if useful, report an observed-subset rate only with its coverage and subgroup label. Keep pending cohorts separate; use `UNKNOWN`, `NOT_MEASURABLE` and `UNDEFINED` for missing baseline, missing observation and zero denominators respectively.
6. Match each conversion numerator to the visitors and observation window eligible to produce it. For delayed verification, use an entry cohort and allow its qualification window to close; do not divide this week's verified contacts by an unrelated week's visits. Attribute each contact once to its last eligible measurable visit/session before `first_qualified_at` inside a fixed lookback (default 7 days) with stable tie-breaks; one session accepts at most one unique-contact conversion and shared-session multi-identity cases go to quarantine. Report first-touch and last-touch as separate attribution views, preserving direct/unknown rather than adding duplicate credit. Unmatched valid contacts remain in the North Star and a separate diagnostic bucket; never use all North Star contacts over analytics-consent-only visits as the matched conversion rate.
7. Keep plan-authoring activity separate from the product baseline. Creating no campaign assets or contacts during document preparation does not prove the operating business has zero assets or contacts.

8. Make the report contract separate state from numeric values: `UNKNOWN` when source/definition is absent, `PENDING` while the entry/qualification/observation window or watermark is still open, `NOT_MEASURABLE` when a closed cohort lacks valid observation/join coverage, `UNDEFINED` only when the defined denominator is truly zero, and `MEASURED` only after a closed, verified cohort. Null/unknown is never zero.
9. Put exact timestamps/windows in the report contract: timezone, entry start, exclusive entry end E, qualification end, observation end, watermark end, snapshot time and cohort version. With qualification lasting 7 full days plus a 24-hour watermark, matched conversion cannot be read before E+8 days; full-cohort Activation-7d cannot be read before the latest qualifying member's Q_end+8 days (up to E+15 days for a qualification window ending at E+7 days). These are earliest-read gates, not guarantees the sample or observation exists. Any read/analysis outside the funded resource period remains pending/deferred until separately staffed and allocated.

List tracking, form/backend, consent verification and CRM work in the build backlog before setting growth targets; a static strategy demo proves none of those systems is live.

## Leading indicators by AARRR stage

After the north star, every plan needs leading indicators per AARRR stage. These move faster than the north star and trigger investigations.

### Acquisition leading indicators
- Organic visits/month, total + per pillar (SEO health)
- App Store / Play Store visit-to-install rate (ASO health)
- Founder-led social channel growth → email subscriber conversion (LinkedIn / X / Substack funnels)
- Event-to-app conversion rate (event ROI)
- Ambassador-attributed visits (referral funnel)
- Paid CAC by channel (when paid is firing)

### Activation leading indicators
- Day 1 / Day 7 / Day 35 → paid conversion rate
- Onboarding session-completion rate
- First key-action completion (post-signup activation event)
- App Store conversion rate (install → trial → paid)
- Trial → paid conversion rate

### Retention leading indicators
- Day 30 / Day 60 / Day 90 retention
- Monthly churn rate (gross + net)
- Lifecycle email engagement (open / click / unsubscribe by flow)
- Hardware → app activation rate (for hybrid businesses)
- Win-back / reactivation rate

### Referral leading indicators
- Ambassador-attributed new subs (via Dub or similar)
- Share-after-value moment rate (% of users sharing)
- Two-sided referral completion rate
- Guides program referrals (when live)
- NPS score (if surveyed)

### Revenue leading indicators
- ARPU by cohort
- Annual plan adoption %
- Cohort LTV by source
- Plan mix shifts
- Eye-mask / hardware attach rate (for hybrid)
- Expansion revenue (B2B)

## Review cadence

The plan should specify three rhythms:

### Weekly (operational sync)
- **Who:** fCMO ↔ founder (CEO usually)
- **Duration:** 30 min
- **Format:** AARRR scoreboard (current vs. last week numbers across the leading indicators) + this week's ships + blockers
- **Output:** Action items, decisions made

### Monthly (metrics review)
- **Who:** fCMO + founder + extended team (CXO, product lead, designer if applicable)
- **Duration:** 60–90 min
- **Format:** Full metrics review + comparison against quarterly KPI targets + qualitative learnings + idea bank reprioritization
- **Output:** Possible plan adjustments, hire decisions

### Quarterly (plan recalibration)
- **Who:** fCMO + founders + key advisors
- **Duration:** 2–3 hours
- **Format:** Full plan review against 90-day and 12-month outcomes, channel-level analysis, funding-stage transition check, recalibration of next 90 days
- **Output:** Updated plan (could be v2 / v3 document iteration)

## KPI target setting

For each quarter in Section 10, the plan must include 3–5 specific KPI targets. These should be:
- **Specific** — not "improve retention," but "Day 30 retention from 22% → 30%"
- **Measurable** — pull from a wired data source
- **Stretch but plausible** — based on funnel state + historical patterns
- **Decision-triggering** — if missed, what does that mean? (Adjust strategy, kill a channel, etc.)

### KPI target patterns by quarter

**Q1 (foundation quarter):**
- Mostly *bedrock* metrics — fixing leaks. "Headphones-gate conversion drop reverses." "Day 1 → paid +25–50%."
- Some *foundation* metrics — laying tracks. "4 SEO pillars staked." "App Store rewrite shipped."
- Avoid bold growth targets — the foundations aren't in yet

**Q2 (validation quarter):**
- Mostly *validation* metrics — does what we built work? "Paid CAC < $X blended." "Organic traffic 1,500–3,500/mo."
- Some *cohort* metrics — do new cohorts behave better? "Day 7 retention for Q2 cohort vs. Q1."

**Q3 (scaling quarter):**
- Mostly *scaling* metrics — how far does it go? "Paid scaling to $20–30K/mo with CAC steady." "First B2B install reference case live."
- Some *capability* metrics — what new things are live? "First Guides pilot launched."

**Q4 (compound quarter):**
- Mostly *compound* metrics — is the flywheel turning? "50%+ of new subs from non-paid channels." "Ambassador-driven 15–25% of new subs."
- Some *narrative* metrics — does the Series A story write itself? "Blended LTV/CAC > 3."

## Anchoring against the VC growth path

For VC-backed clients past $1M ARR, anchor 12-month and multi-year targets against the **3-3-2-2-2 rule** (3× in years 1 and 2, then 2× in years 3 through 7). Hitting it is rare; most companies don't. Anchoring against it forces the plan to either match it and show how, or explicitly defend choosing a slower trajectory. Full table and context in `growth-patterns.md`.

For non-VC-backed companies (bootstrapped, founder-funded, profit-focused), the 3-3-2-2-2 doesn't apply. Use linear-pattern targets ("$X MRR added per month") or step-function targets ("$Y revenue jump after the enterprise tier launches") instead.

## Forecasting reality check

A plan derives a budget and an annual goal. It does not produce a 12-month month-by-month forecast that's reliably accurate to the dollar.

**Unless the company is publicly traded, all forecasts are educated guesses.** No startup under $100M ARR consistently hits month-by-month forecasts. Quarterly review is when the plan adjusts — not when variance is treated as failure.

What the plan commits to honestly:
- The annual goal is a defensible direction-of-travel
- The budget is the resource commitment that makes the goal plausible
- The 90-day roadmap (Section 9) is what's actionable now
- Month-to-month projection is illustrative, not promised

Founders who over-engineer the forecast end up explaining variance every month instead of executing. The plan should resist this — name the annual target, the quarterly KPIs, and the kill criteria. Don't promise the month.

Full context in `budget-planning.md`.

## Kill criteria

For every channel or initiative, the plan should specify when to stop. Often missing from plans, kill criteria force discipline.

Examples:
- "If a paid channel has CAC > 2× target after 30 days at meaningful spend, pause."
- "If onboarding Variant 3 doesn't show statistically meaningful lift (or directional lift + congruent qualitative signal) after 4 weeks, move to Variant 1."
- "If lifecycle Flow 4 has open rate < 12% after 6 weeks, redo subject lines + audience segmentation."

## Guardrail metrics

Some metrics get a hard guardrail (cannot drop below threshold). Useful for protecting brand or unit economics during aggressive growth.

Examples:
- "Brand voice complaint rate > 1% of customer feedback triggers content review."
- "Paid CAC > $X for two consecutive months pauses paid scaling pending audit."
- "App Store rating drops below 4.5 triggers product review."

## Data sources mapping

The plan should name where each metric comes from. This makes it auditable.

| Metric | Source |
|---|---|
| Organic traffic | GA4 / Ahrefs |
| App Store conversion | App Store Connect |
| Funnel conversion (Day N → paid) | Internal analytics (Mixpanel / Amplitude) or App Store Connect cohort export |
| Retention | Customer.io segments + product analytics |
| MRR / ARR | Stripe (via MCP if wired) |
| Plan mix | Stripe |
| Lifecycle email metrics | Customer.io |
| Ambassador attribution | Dub.co |
| Hardware → app activation | Shopify + App Store + internal join |
| NPS | Survey tool (Customer.io / Typeform / SurveyMonkey) |

## When data isn't wired

If a metric can't currently be measured, flag it in Section 13's open decisions. Example:

> "Hardware → app activation rate not currently visible in the App Store dashboard. Requires Shopify ↔ App Store Connect join. Q1 work item."

A plan with un-measurable goals is a plan that can't be validated. Surface the instrumentation work explicitly.

## Reporting cadence + automation

Where possible, auto-generate the metrics review rather than building it manually each time. Stripe MCP + GA4 MCP + Customer.io MCP can pull most of what's needed.

For Tier 1 clients, a simple weekly metrics email to the team (Markdown table, generated via skills + MCPs) costs nothing and creates discipline.

For Tier 2+ clients, consider a real dashboard (Hex, Metabase, Looker, or internal tool).
