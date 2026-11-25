---
name: opa-content-workspace-design
description: Use when designing OPA plan or content workspace websites.
---

# OPA Content Workspace Design

## Scope
Apply the user's preferred presentation to OPA/Huy strategy, content libraries, implementation plans and Vercel document sites. Primary design reference: https://opa-rebuild-at-32-v9.vercel.app/ . For explicit exact-match requests and Huy-only scripts, load [Exact V9 parity](references/exact-v9-parity.md); do not substitute a merely inspired redesign or infer sole-founder history. Earlier reference https://rebuild-at-32.vercel.app/ remains a secondary master–detail option, not the default. For requests for actual content to film, load [Recording library](references/recording-library.md): topic plans are not filming deliverables; prioritize clean narration, director and scene/caption access in a polished production library. This is a presentation preference, not authority to rewrite strategy, produce social copy, approve gates or deploy. Follow a newer explicit design brief instead when provided.

## When to Use
Use for OPA/Huy plans, research libraries and content workspaces, including requests to re-export an existing plan to Vercel after a design change. Treat that continuation as a request to apply the chosen design and redeploy, not merely return the unchanged URL.

## Procedure
1. Read the actual plan, research and existing site's generator, CSS, JavaScript and verification script. Inspect the supplied reference's rendered layout and interactions before adapting its general pattern.
2. Preserve the source documents and back up the current implementation outside the upload directory. Inspect the existing `.vercel/project.json` to identify the intended project before changing a live site.
3. Implement the composition below as one coherent build. Update the authoritative generator and its assets together: editing generated JavaScript alone leaves old HTML incompatible, while a stale generator can overwrite a redesign on rebuild. Keep one documented build entrypoint and exclude build/test scripts and backups from deployment.
4. Establish the publication boundary before mapping sources. For internal attachments, publish only a reviewed shareable derivative; keep raw documents, security findings, personnel records awaiting consent and unreviewed legal text out of the upload directory and downloads. Preserve the complete approved-for-sharing derivative, qualifications and provenance. For already public/shareable source documents, preserve wording and downloadable originals. Map sections with stable document/section keys rather than numeric positions, because inserting a section can silently route later items into the wrong module. Prefix generated IDs and verify rendered text against the intended publication source.
5. Rebuild and exercise the resulting interface before deployment. When new strategy supersedes an earlier plan, default to the new module and visibly mark retained baseline calendars as archived/superseded; preserving old text must not present conflicting instructions as current. Test every advertised interaction: search is not a category filter, a Markdown task list is not an interactive checklist, and displaying an inventory is not structured filtering. Treat delegated completion as a handoff to inspect, not evidence that build and tests ran. If a child returns partial changes, reconcile them into a working artifact before uploading.
6. When publication is requested, follow [references/vercel-static-workspaces.md](references/vercel-static-workspaces.md). Verify the live alias and report the working link with only features actually tested.

## Composition contract
Default to a **Decide / Learn master playbook with an Explore library**, following the V9 reference's general hierarchy. Do not force the previous two-column selector UI onto every export.
1. Compact sticky topbar: identity, descriptive subtitle, quick section anchors, real version badge; presentation-mode action when implemented.
2. A substantial opening banner explains the document's purpose and reading route. Use meaningful metadata pills and summary tiles drawn from actual content, not fabricated counts or success claims.
3. Follow with full-width section panels: positioning/strategic frame → overview matrix/calendar → detailed topic or project cards → implementation/funnel/KPI. Preserve sources and evidence qualifiers alongside claims.
4. Collections get category chips, search and overview tables linking to corresponding detail cards. Cards have ID, phase, audience, duration/status only where supplied, a clear title, and separated content blocks. Script-specific blocks (voice, clean narration, shot breakdown) appear ONLY if scripts were supplied or separately commissioned through required gates.
5. Add copy controls with success/error feedback, source download and print. Offer presentation mode with keyboard navigation and a truthful slide count when built and tested; never advertise an unimplemented control. Use master–detail only for a collection that genuinely benefits from it.
6. Responsive topbar and horizontal tables; 44px touch targets; readable body text, no page-level overflow. Print shows all relevant content. Local checklist state, if implemented, is explicitly browser-only and never a Telegram/QA/Sheet approval.

Treat V9 as design authority, not proof of product capability. When Huy identifies its manuscripts as his own, use them as attributed source drafts, not merely visual inspiration; do not treat unsupported performance claims or self-awarded scores as verified. Do not infer that another plan inherits the same biography, audience or production method.

For Huy's filming library, feature HUY alone throughout titles, narration, director notes, visuals, captions and downloads. Remove collaborator/meeting scenes without crediting collective technical work personally to Huy or implying sole-founder history. Preserve Vietnamese phrases such as “chứng minh”, “thông minh” and “minh họa”; never use a blind case-insensitive name replacement. Keep the original private and generate a revised derivative with a change log.

The latest exact-match preference takes precedence over the earlier dark palette: for this V9-derived library use the reference's actual light surfaces, blue/green hero, typography, full-width sections, overview tables and complete script cards. Do not substitute a dark two-column master–detail redesign. Keep the earlier palette below only as an alternative when explicitly requested.

For future requests to export OPA content to a Vercel link, use this V9-style playbook by default, deploy only the requested artifact, verify the stable live URL and return the clickable public link. Saving this preference alone does not authorize changing an existing deployment.

## Alternative palette — earlier dark brief
Use only when explicitly requested instead of exact V9 fidelity. Black is dominant; orange is primary emphasis; blue is secondary.

| Token | Value | Role |
|---|---|---|
| background | #080C14 | Main near-black canvas |
| surface | #0F172A | Header and secondary panels |
| card | #131F37 | Reading and selector surfaces |
| border | #263449 | Subtle separators |
| text | #F1F5F9 | Main text |
| muted | #AAB8CB | Secondary readable text |
| orange | #F97316 | Primary buttons, active tab, emphasis |
| blue | #38BDF8 | Links, secondary headings, focus |

Use near-black text on solid orange or blue controls. Keep most area dark; no orange full-page background, rainbow headings, glossy gradients or invented metrics. Check actual contrast when changing combinations.

Typography: Vietnamese-capable humanist sans (prefer Be Vietnam Pro when licensed/available), mono for IDs/metadata. Body 16px minimum, line-height 1.7–1.8; panel padding 24–32px desktop, 16px mobile, radii 8–12px. Bundle fonts or use fallbacks if remote assets conflict with CSP.

## Fidelity and verification
Preserve complete intended content, budget units, qualifiers, sources and downloads. For user-owned exact-match references, reuse their actual layout/CSS and authorized assets, while adjusting scope truthfully; otherwise adapt the pattern without copying identity or assets. Never advertise 60 scripts when only 30 exist. Avoid empty hook/script modules.

For script edits, check all layers together: title, clean narration, director, setup, scene dialogue, caption and download. Reconcile narration with the scene dialogue; neutralize contradictory unmeasured timings or deliverable counts instead of inventing a new number. Run independent editorial review for sole-founder inference, reassigned technical credit and other people's likeness requirements before deployment; a name scan alone misses these semantic regressions.
Before finishing, test desktop, tablet and narrow mobile, tab/list selection, keyboard focus, search, copy feedback/failure, checklist persistence where present, source download and all-content print. At each width, compare document scrollWidth to viewport width and inspect overflowing elements: a large reference image can fit desktop/mobile overrides yet overflow tablet. Constrain images with max-width:100%; height:auto and confine wide tables to horizontal scroll containers. If exact-source CSS is validated by prefix/hash, append responsive overrides after the preserved source rather than prepending them and breaking the fidelity assertion. Rebuild and rerun checks after any repair. Verify no missing sections. For deployment requests, use the intended project and read back the exact live URL before claiming success. A saved skill alone does not update an existing site.
