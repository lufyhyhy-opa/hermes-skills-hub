# Deploying and verifying static workspaces on Vercel

## Preflight
- Run `vercel whoami`; use the authenticated account without exposing tokens.
- For updates, inspect `<site>/.vercel/project.json` and preserve its project link. For a new plan, use a separate directory/project rather than overwriting another showcase.
- Read `vercel.json` and `.vercelignore`. Keep deploy artifacts limited to HTML, CSS, JavaScript and intentional downloads; exclude source generators, verification helpers, backup copies and internal manifests.
- A static site can use `framework: null`, `buildCommand: null`, `outputDirectory: "."`. Generate final assets locally before deployment. Use external script/style files if CSP allows only `'self'`; inline event handlers will be blocked.

## Build and acceptance
1. Run the project's documented generator; check JavaScript with `node --check <site>/site.js`.
2. Verify source downloads byte-for-byte and rendered text section-by-section, including research and source lists. Count selector targets and panels, validate every target, and check unique IDs.
3. Test desktop and a narrow mobile viewport. Exercise tab switching, selecting another item, accent-insensitive Vietnamese search, empty results and recovery. Check page-level overflow independently of intentional table scrolling.
4. Exercise clipboard success/error handling and all-content print. Hidden selected panels must become visible in print; a hidden parent article can otherwise suppress an entire document. Report only the checks actually exercised.
5. Rebuild once more to ensure the generator reproduces the same working UI rather than restoring stale assets.

## Publish
For an existing linked project:

```sh
vercel deploy <site-directory> --yes --prod
```

For a new project, run deployment in its isolated directory and inspect the created project and production alias before continuing. Do not infer that the provider console URL is the public reading URL.

## Read back
- After deployment reaches READY, fetch the exact stable `https://<project>.vercel.app/` alias, not just the immutable deployment URL.
- Check HTTP success and compare response bytes to local HTML, CSS, JS and downloadable originals. This detects a successful deploy whose alias still serves an older artifact.
- Open that live alias in the browser and repeat the critical tab/list/search interactions. Note which viewport sizes and controls were actually tested.
- `X-Robots-Tag: noindex, nofollow, noarchive` and `robots.txt` discourage indexing; they do not restrict access. State that anyone with the link can read it unless authentication was separately configured.

## Delivery
Return the stable public URL, a short description of the applied layout, preserved content and verified behavior. A design-only change or local checklist does not authorize social publishing or complete Telegram/QA gates.
