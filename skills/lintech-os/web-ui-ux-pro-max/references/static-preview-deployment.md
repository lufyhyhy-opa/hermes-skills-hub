# Static dashboard previews on Vercel

Use for a public link to an existing report or lightweight interactive dashboard. Keep this path static when the acceptance criterion is view/filter/download: a frontend framework, server function and live-data service are unnecessary for a snapshot.

## 1. Establish the publication boundary

1. Read the actual report/artifact and determine whether it contains public data or private account information.
2. Export an allowlisted static directory: `index.html`, local CSS/JS, sanitized report JSON, optional report download, and `vercel.json`.
3. Preserve source observation time and N/A values; label the page **snapshot**. Do not invent price charts, manufacture missing rows, or imply live refresh from a deployment timestamp.
4. Keep model results distinct from verified facts. Expose material assumptions alongside the labels instead of silently changing the research engine while publishing its UI.
5. Show valid history only. Omit same-period reruns and fixture-to-real comparisons from a weekly-change view.

## 2. Discover the authenticated deployment target

```bash
vercel --version
vercel whoami
vercel teams ls
vercel project ls
```

Use the observed scope. A preview request does not authorize overwriting an unrelated project's production deployment. For a new isolated dashboard project, bind the directory explicitly:

```bash
vercel project add "$PROJECT" --scope "$SCOPE"
vercel link --yes --project "$PROJECT" --scope "$SCOPE" --cwd "$SITE_DIR"
vercel project inspect "$PROJECT" --scope "$SCOPE"
```

Resolve authentication through the approved user authorization flow if needed; never ask for tokens in chat. Do not save a session's team name or project identifiers as reusable defaults.

## 3. Inspect exactly what will upload

`vercel link` can create local environment files or download authentication material. Exclude these before deployment; deploying only a safe-looking source folder is not enough after linking it.

Example `.vercelignore`:

```text
.git
.env*
.vercel
node_modules
*.log
```

Then inspect the real file manifest:

```bash
vercel deploy --dry --yes --json --cwd "$SITE_DIR"
```

Run this after linking: the CLI may need a linked project even for dry inspection. Confirm only intended public files appear. Exclude source config, local credentials and unrelated repository files. Keep secret scanning/manifest evidence out of the public directory.

For a dependency-free static site, explicitly set `framework: null`, `buildCommand: null`, and `outputDirectory: "."` in `vercel.json`. Add `X-Robots-Tag: noindex, nofollow` for previews; this controls indexing, not access. Align CSP with actual assets: self-host resources or declare the required origins rather than leaving a blocked external-font import.

## 4. Exercise the UI before deployment

Follow `webapp-testing` for browser execution. For static files a local HTTP server is sufficient; load via HTTP rather than `file://` when JS fetches report JSON.

- Verify unique table-row count against the exported source programmatically.
- Test search, signal/sector filters, sort, empty/reset, detail modal, and download.
- Keep visible numbers in tabular/monospace type; use enough precision that small-price support bands do not collapse into identical rounded endpoints. Preserve the source's precision limitations rather than inventing extra digits.
- Test a desktop width and a narrow mobile width. Confirm the table scrolls inside its region while the document itself does not widen.

### Fixing hidden-label overflow

Check all three widths: `screen.width`, `innerWidth`, and `document.documentElement.scrollWidth`. A mobile layout may have a 390px screen but a much wider visual/document viewport, making the whole page look tiny.

Inspect bounding boxes before adding global overflow rules. An absolutely positioned `.sr-only` label inside a far-right table cell can escape the intended scroll container. Establish its containing block on the scrolling region:

```css
.table-scroll {
  position: relative;
  overflow-x: auto;
}
```

Retest at the same narrow viewport and require document width to match viewport width. Preserve keyboard/screen-reader labels and table scrolling; do not hide the symptom with root `overflow-x: hidden`.

## 5. Deploy and read back the exact deployment

```bash
vercel deploy --yes --scope "$SCOPE" --project "$PROJECT" --cwd "$SITE_DIR"
```

Use the default preview environment when appropriate. To give a publicly accessible stable alias for a **new isolated preview project**, explicitly use `--prod`; this deploys the demo to that project's production environment, not to an existing product. Do not disable team-wide protection merely to share one demo.

Read the returned immutable URL and deployment ID, then verify remote state:

```bash
vercel inspect "$DEPLOYMENT_URL" --scope "$SCOPE"
```

Require `Ready`, and check the actual alias to share using unauthenticated HTTP GET plus a browser. A deployment can be Ready yet show an authentication wall.

Verify:
- Root HTML, JS, CSS, JSON and download respond successfully.
- Downloaded JSON matches local sanitized data (hash or parsed comparison); row count and unique count match the source.
- Secret paths such as `/.env.local` are not public; this complements, not replaces, the upload-manifest inspection.
- Search/details work at the public URL and mobile width is still correct after the final deployment.

Rerun remote checks after any last-minute CSS or data fix; local success does not verify the published revision. Stop the local test server after public verification.

## 6. Handoff

Lead with the verified clickable alias. Briefly state what the user can inspect and whether the page is snapshot/live. Explicitly distinguish a working hosted preview from scheduled regeneration or GitHub integration, which need their own deployment pipeline. Save deployment handles in project documentation, not this skill.
