---
name: social-channel-research
description: "Use when researching a social creator page or share URL."
version: 1.0.0
author: LinTech Autonomous Council
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [social, facebook, tiktok, instagram, youtube, creator, channel-research, content-dna, collab]
    category: research
    related_skills: [grounded-citations, blocked-page-recovery, ghosttrack-osint, marketing-plan, huy-intent-and-gold-standards]
---

# Social Channel Research (Creator / Page Dossier)

One-shot research of a social creator or page into a **decision-ready dossier**: identity, cross-platform map, content DNA, monetize signals, risks, and next probes. Built for Anh Huy short orders (`nghiên cứu kênh này`, share link, handle).

## When to Use

- Share/post URL (FB `share/…`, Reel, Short) or bare handle/page name
- "Soi page / research channel / collab check / học pattern short-form"
- Competitor or reference creator before seeding, booking, or cloning mechanics

**Not for:** recurring company news watches (`competitor-news-monitor`); pure username existence sweep without content DNA (`ghosttrack-osint` username API is a helper only); reverse-engineering a single video into generation prompts (`ai-video-prompt`).

## Output contract (always)

Write `~/marketing-plans/research-<slug>/BAO-CAO-….md` **and** a terse chat snapshot (tables + numbers). Package must include:

1. Identity table (canonical URL, followers, category, geo, page/channel IDs, created date if public)
2. Post/object that triggered research (caption, format, partial engagement + **logged-out caveat**)
3. Cross-platform map (every linked + discovered handle + scale)
4. Content DNA (niche, hook formula, hashtag stack, length, repurpose pattern)
5. View distribution sample (list raw numbers; compute min/median/max — never invent ER%)
6. Operator signals (booking email, agency/MCN, multi-admin, ads on/off)
7. AI/authenticity signals with **confidence band**, not binary claim without frame QA
8. Strengths / risks / map-to-Anh-Huy-goal (collab vs pattern-borrow vs no-fit)
9. Next probes table (login scrape, vision QA, Ad Library, rate card)
10. Sources touched + explicit **coverage gaps**

Tone: short sentences, markdown tables, quantitative. No AI-slop openers.

## Procedure

### 1. Resolve the object

- FB `facebook.com/share/…` → open with **`browser_exec`** (not `web_extract` alone). Share links resolve to page or post; capture final `location.href` + `document.title`.
- Extract caption/hashtags from attached context and live DOM `innerText`.
- If URL is already a page/handle, still open live browser for About/Reels/transparency.

**Pitfall:** `web_extract` on Facebook often returns title + one caption line only. Treat extract as a seed, never the dossier.

### 2. Page / profile core fields

Browser tabs in order:

| Step | FB path | Capture |
|---|---|---|
| Home | `/<vanity>` | followers, following, intro, latest post teaser |
| About | `/<vanity>/about` or Contact info | category, address, websites/social links, hours |
| Transparency | About → Page transparency | Page ID, creation date, ads running?, multi-admin note |
| Reels | `/<vanity>/reels/` | visible view counts list (sample 8–15) |

Also run parallel `web_search` on exact page name + "followers" / booking domain.

**Pitfall:** Logged-out FB hides full reactions/comments/shares and may under-count. Label every engagement figure `logged-out partial` — never compute ER% from partial numerators over full follower denominators.

### 3. Cross-platform expansion

From About social links **and** name variants, open/extract:

| Platform | What to get |
|---|---|
| TikTok | handle, bio, followers/likes if visible |
| Instagram | handle, followers if visible |
| YouTube | every channel with same brand string — subs, video count, Shorts view sample, About/booking |
| Email / domain | booking@… → search operator company (MCN/agency) |

Username sweep helper (optional): GhostTrack `POST http://127.0.0.1:8192/api/track-username` with the vanity string.

**Pitfall:** TT/IG often bot-wall headless browsers. Record **gap**, keep linked handle, do not fabricate follower counts. Retry once with longer wait; then move on.

**Pitfall:** Same brand often has **multiple YT channels** (main, shorts dump, AI-named alt). List all; note handle tokens like `AI` as authenticity signal, not proof.

### 4. Content DNA

From captions + titles across platforms, extract:

- Niche one-liner
- Hook pattern (length, structure: situation / punchline)
- Fixed hashtag stack vs rotating tags
- Format (Reel/Short length band)
- Repurpose behavior (same caption mirrored FB↔YT within hours)

View sample: paste the raw reel view list; report min / median / max. Sidebar "Popular videos" multi-ten-million labels need **per-URL open** before treating as verified lifetime views.

### 5. Operator & monetize read

Score signals (present/absent):

- Professional booking email / agency domain
- Multi-admin + category Personal blog at multi-million follow
- Ads currently running (transparency)
- Funnel depth on captions (pure TOFU vs link-in-bio sell)
- Brand-safety: unlabeled AI-looking volume, child-adjacent content, policy risk

Agency domain → one `web_search` / extract on that brand for scale (subs, positioning).

### 6. Authenticity band (not courtroom verdict)

Use a **confidence band**: low / mid / high for "AI or hybrid factory" vs "mostly filmed UGC".

Positive AI/hybrid signals: AI token in handle; identical punchline templates at high volume; global AI-baby/template wave fit; agency factory multi-channel mirror.
Positive real-UGC signals: consistent real locations/voices across years; behind-the-scenes long-form; verifiable people off-platform.

Without frame-level vision QA on several clips, **do not** state "this is AI" as fact — state band + what would falsify it.

### 7. Map to requester goal

Before closing, one explicit section:

| Goal | Verdict rule |
|---|---|
| Collab / seeding | booking path + rough package value band only if evidence; else "need rate card" |
| Steal short-form mechanics | list 3–6 portable mechanics (hook length, hashtag discipline, cross-post SLA) |
| Audience fit vs Anh Huy product (e.g. webgame 18+) | say **no-fit** when demography diverges; forbid forced persona copy |

### 8. Deliver + gaps

- Save markdown under `~/marketing-plans/research-<slug>/`
- Chat: snapshot tables first, path via `MEDIA:` if useful
- End with coverage gaps and optional next probes (login ER scrape, vision QA ×5, Meta Ad Library by Page ID, email rate card)

## Tool order (default)

```
parallel: web_extract(share_url) + web_search(page name)
→ browser_exec: open final URL, About, transparency, Reels (batch reads)
→ parallel: YT/TT/IG extract + web_search(booking domain) + optional GhostTrack username
→ write dossier + chat snapshot
```

If browser blocked → `blocked-page-recovery` ladder; still never invent metrics.

For claim-heavy partner decks, register URLs with `grounded-citations` `sources.py` while fetching.

## Pitfalls

- Treating one viral sidebar view count as median performance — use a sample list.
- Equating followers with reach — report both followers and view distribution.
- Calling multi-admin page a "mom blog" without booking/agency check.
- Filling TT/IG blanks with guesses after bot wall.
- Mapping entertainment TOFU baby audience onto unrelated product demography.
- Stopping after FB home scroll — About + transparency + Reels are mandatory for a complete dossier.

## Verification checklist

- [ ] Canonical page URL + at least one stable ID (Page ID or channel id/handle)
- [ ] Cross-platform table with explicit gaps
- [ ] Raw view sample present (or stated unavailable)
- [ ] Engagement numbers labeled if partial/logged-out
- [ ] Authenticity stated as band + falsifiers
- [ ] Next probes listed only for missing high-value facts
- [ ] File written under `~/marketing-plans/research-<slug>/`
