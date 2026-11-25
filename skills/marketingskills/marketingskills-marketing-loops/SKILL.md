---
name: marketing-loops
description: "When the user wants a recurring marketing job an AI agent runs on a cadence or trigger, or asks what a weekly or daily automated check should do, remember, and when it should stop: SEO and ads checks, churn watches, outbound triage. For one-off ideas, see marketing-ideas. For the test loop, see ab-testing."
metadata:
  version: 1.8.5
---

# Marketing Loops

You help set up **marketing loops** — repeatable marketing workflows an AI agent runs on a cadence, each with a defined trigger, a bounded set of steps, a self-check, and an explicit stopping condition. A loop turns a marketing task you'd otherwise do manually (and forget) into an always-on system: the weekly SEO opportunity scan, the ad-fatigue refresh, the churn-signal watch.

This is the operational cousin of `marketing-ideas`. Ideas tell you *what to try once*. Loops tell you *what to keep doing on a schedule* — and wire the other marketing skills together to do it.

## How to Use This Skill

**Check for product marketing context first:** if `.agents/product-marketing.md` exists (or `.claude/product-marketing.md`, or the legacy `product-marketing-context.md`), read it before asking questions. Use that context and only ask for what's missing.

Then:
1. **Clarify the job.** What outcome should this loop protect or grow? (rankings, ad efficiency, activation, retention, revenue, referrals)
2. **Pick a loop** from the catalog in `references/loop-catalog.md` — or adapt the closest one.
3. **Tune the cadence** to signal speed and the complete production/review capacity (see the cadence rule below). For continuous multichannel content, use the capacity-first recipe in `references/loop-orchestration.md`; checking or generating drafts more often does not create additional publishable output.
4. **Confirm the human checkpoint.** Decide what the loop does autonomously vs. what it stages for human approval before publishing or spending — see `references/loop-guardrails.md`.
5. **Build the destination capability matrix.** For each account and format, record documented official support, native/manual fallback, required permissions/review, connection status and live UAT status separately. Check current canonical documentation before promising cross-channel auto-posting; native scheduling and admin consent do not establish API support. Use the `grounded-citations` current-capability reference for source conflicts.
6. **Exercise the authorized scope.** A planning request ends with staged specifications, explicit stop conditions and an inactive rollout proposal. An implementation request needs its approved prerequisites and sandbox tests before activation. Schema/fixture checks are not proof of live approvals, permissions or publication.
7. **Schedule only the authorized loop** after its destination tests, review capacity and kill/reconciliation path are established (see "Scheduling a loop" below).

Building more than one loop, or a whole marketing operating system? See `references/loop-orchestration.md` for how loops compose and the order to adopt them (start with tracking + a weekly review; don't build them all at once).

## Anatomy of a Marketing Loop

Every loop in the catalog has these nine parts. When you author or adapt one, fill all of them — a loop missing a stop condition, a self-check, or its state handling is a liability, not an asset.

| Part | What it defines |
|------|-----------------|
| **Check cadence** | How often the loop *looks* (weekly / daily / on-trigger). Match it to signal speed. |
| **Acts when** | The action condition — what must be true to actually *do* something, vs. just check and skip. Most runs of a good loop are "checked, nothing to do." |
| **Purpose** | The one outcome this loop exists to move. |
| **Skills used** | Which marketing skills the loop orchestrates each iteration. |
| **Loop body** | The ordered steps run each iteration. |
| **Self-check** | The verification done *before* acting — so the loop doesn't act on noise, seasonality, or a tracking bug. |
| **State / idempotency** | What the loop remembers between runs: last-run marker, dedupe key, cooldown window, "already handled" set. Without this, loops double-act, re-nag the same people, or re-alert the same thing. Non-negotiable for anything scheduled — see `references/loop-state.md` for where state lives and the idempotency patterns. |
| **Stop / bail-out** | When the loop skips, halts, escalates to a human, or disables itself — plus what it does on error. Every loop needs one, including heartbeat loops (their stop is "manual disable + error-halt," never "n/a"). |
| **Output** | Where results go: a file, a PR, a staged draft, a notification, a report. |

The **Check cadence / Acts when** split matters: a churn-signal loop might *check* daily but only *act* when an account crosses a risk threshold it hasn't been contacted about inside the cooldown window. Conflating the two produces loops that either miss the window or spam.

## The cadence rule

Match cadence to how fast the signal actually changes — not to how often you'd *like* an update.

| Signal | Realistic cadence | Why |
|--------|-------------------|-----|
| Rankings, backlinks, domain authority | Weekly | Move slowly; daily checks are noise |
| Ad creative fatigue, CPA drift | Every 2–3 days | Meta/Google feedback loops are days, not hours |
| Activation / onboarding funnel | Weekly | Needs enough signups to be significant |
| Churn signals | Daily or on-trigger | Early intervention window is short |
| Content / copy decay | Monthly | Traffic erosion is gradual |
| Competitor changes | Weekly | Pricing/positioning shifts are infrequent but matter |
| Social listening / mentions | Daily | Engagement windows close fast |

Over-frequent loops are the most common failure mode: they generate busywork, burn budget, and train you to ignore the output.

## Continuous multichannel content

For Anh Huy's continuous-content requests, present a recurring production and distribution system with concrete outputs, tools and human responsibilities. Define continuous as a replenished source backlog, batch production and an approved queue; use daily publishing only when the capacity model supports it.

- Count full packages, unique creatives, individual asset components, destination placements and QA coverage separately. Include the seed/canary in the chosen package ceiling; cross-posting one master does not create multiple original videos.
- Cost sourcing, editing, required formats, independent QA, human approval, destination checks and community service before choosing a cadence. Build separate setup-period and steady-state capacity tables: landing/backend/CRM/tracking/templates/SEO setup consumes first-period hours and cash, so reduce or defer content accordingly. Price additional cuts and destinations against the remaining capacity rather than treating them as free AI output.
- Build from real, rights-cleared source material. AI may draft scripts, captions, subtitles, layouts and summaries; source footage, factual verification and approval remain assigned responsibilities. Missing required raw material holds the video branch.
- Keep QA genuinely independent: copy/fact reviewer must not be the writer, and video/vision reviewer must not be the editor; bind each certificate to the exact content version and destination package. If staffing cannot separate roles, label the check as self-review and keep the independent gate blocked rather than presenting it as passed.
- Bind every human approval to the exact payload/version, destination and proposed slot; any change invalidates that receipt. Preserve the configured rewrite/render limits, record counters, and escalate when exhausted instead of silently retrying or waiving QA.
- Select existing tools first, prove one package and one destination manually/native, then add only the automation that removes a measured bottleneck. Keep documented capability, account permission, connection and live verification as separate states.
- Show the baseline and growth scenarios as proposals, with no claimed automation percentage, output guarantee or implied extra budget. Preserve all required approvals; a plan or demo request leaves production and sending loops inactive.
- For planning/demo operator packs, ship **offline queue contracts + a pure simulator** before any scheduler. Allowed terminal states only: `HOLD`, `RECONCILE`, `SKIP_DUPLICATE`, `SUPPRESS`, `HALT`, `READY_FOR_MANUAL_HANDOFF` / `READY_FOR_MANUAL_REVIEW`. Never emit `PUBLISHED`, `SENT`, or `SPENT` from the simulator. Every result sets `side_effect_performed=false` and `dispatch_allowed=false`; the simulator performs zero network/OAuth/CRM/cron side effects. Fixture-green is not live permission. Collect all blockers before choosing a primary decision so conflicts remain visible; apply precedence: kill switch → `HALT`; unknown side-effect state → read-only `RECONCILE` (never blind-retry); known-state suppression/no purpose consent → `SUPPRESS`; duplicate idempotency key → `SKIP_DUPLICATE`; any remaining malformed item, QA, approval, permission or authorization blocker → `HOLD`; only no blockers → `READY_FOR_MANUAL_HANDOFF`. The primary label never clears other blockers and never permits dispatch. Bind approval to exact action, package/content ID, version, channel, destination, slot and payload hash; require execution authorization as a separate exact boolean. Keep four contracts separable: intake staging, repurpose package assembly, publish-stage (approved slots only), weekly learn/report — all default `INACTIVE` until an explicit final command plus destination UAT receipt.

## When NOT to loop

Not everything should be automated on a cadence. Skip a loop — or add a mandatory human checkpoint — when:

- **Strategy or creative direction is the real work.** Loops maintain and optimize; they don't set positioning, invent campaigns, or make brand calls.
- **The action publishes or spends without review.** Auto-*drafting* an ad, email, or post is fine. Auto-*publishing* or auto-*shifting budget* needs a human checkpoint unless the user has explicitly authorized autonomous action and set guardrails (caps, allowlists).
- **The signal is too sparse to be significant.** A weekly conversion-rate loop on 40 visitors/week is measuring noise.
- **It's a vanity loop.** If nobody acts on the output, delete the loop. A loop that emails a dashboard nobody reads is worse than nothing.

For any loop that sends, spends, publishes, or touches personal data, apply `references/loop-guardrails.md` — the two-tier action model (autonomous-safe vs. gated), spend/send caps, CAN-SPAM/GDPR/FTC/ToS rules, the always-escalate list, and a required kill switch.

## Scheduling a loop

These loops are agent-agnostic — the *body* works in any agent. The *scheduling* depends on your environment:

- **Claude Code** — native options: `/loop` (self-paced, until a condition), `ScheduleWakeup` (dynamic pacing that reacts to state), and `CronCreate` (fixed cron schedule). If you have a loop-mechanics skill such as `loopify` installed, use it to choose between them and tune delays; otherwise the guidance below is enough.
- **Any agent + cron** — wrap the loop body as a scheduled prompt/script (`0 9 * * 1` for Mondays 9am, etc.).
- **Manual cadence** — for high-judgment loops, "run this skill every Monday" is a perfectly good loop. The value is the repeatable *body*, not the automation.

Default to time-of-day cron for review-style loops (weekly review, ranking watch) and dynamic pacing for monitor-until-threshold loops (churn watch, launch-day tracking).

## The Catalog

`references/loop-catalog.md` holds the full library — 60 marketing loops with thorough funnel coverage: SEO & Content, Paid, Earned/Social/Partnerships, Outbound, Activation, Retention, Revenue, Referral & Advocacy, and Ongoing Ops. Each is a complete, adaptable spec. Start there, pick the closest match, and tune it to the user's product, stage, and tooling.

## Running a whole channel: the SEO operator

When the user wants an agent to own SEO for a site rather than run one loop, use `references/seo-operator.md`. It bundles the SEO loops (site health, claim drift, striking-distance push, AI-answer check, keyword gap, content decay, competitor watch, and more) into one schedule with shared memory in `.agents/seo/`, a first-run checklist, operating rules, a writing gate, and a one-screen weekly report.

## Running outbound: the outbound operator

For an agent running day-to-day outbound (signal sweeps, staged outreach, reply triage, sending-domain health, weekly sequence retros), use `references/outbound-operator.md`. It sets the brief, approved claims, approval rules by tier, shared memory in `.agents/outbound/`, and a weekly report.

## Authoring a new loop

When nothing in the catalog fits, author a new loop from `references/loop-template.md` — a copy-paste template with fill-in prompts, a worked before/after example, and a ship checklist. Fill all nine anatomy parts; if you can't answer the self-check, state/idempotency, and stop/bail-out concretely, the loop isn't ready to run.

## Anti-patterns

- Looping without a stop condition → runaway spend or infinite churn.
- Same cadence for every loop → most run too often and get ignored.
- No self-check → the loop acts on noise, seasonality, or a tracking bug.
- No human checkpoint on spend/publish actions.
- Building 10 loops at once → start with one, prove it earns its keep, then add the next.

## Banned vocabulary

Avoid: "set it and forget it," "fully autonomous marketing," "AI does everything," "10x on autopilot," "growth hacking machine." Loops are disciplined systems with checkpoints, not magic. Describe them honestly.

## Related Skills

- **marketing-ideas** — one-off tactics and inspiration (what to try). Loops operationalize the ones worth repeating.
- **ab-testing** — the experimentation loop specifically (hypothesis → test → promote winner → repeat).
- **analytics** — most loops read from analytics to decide whether to act.
- **reverse-engineer-marketing** — the growth-move watch loop keeps a competitor teardown current, and teardown plays name the loop that sustains each one.
- Individual channel skills (`ads`, `seo-audit`, `emails`, `social`, `churn-prevention`, `pricing`, `referrals`) — the loop bodies orchestrate these.
