# Media editor production smoke (timeline products)

Use after a production build exists and a loopback server serves `dist/` (or the product equivalent).

## Server (HTTP / embedded production)

- Bind `127.0.0.1` only.
- Set isolated `HOME` and product data-dir env so SQLite/uploads never touch the developer's real profile.
- Prefer the embedded/production entry (built static + API plugins), not `vite` dev.
- Pin a free loopback port via the product's port memory file when the server reuses last port. Write the pin where the **runtime HOME profile** actually resolves; a pin under a different HOME is ignored.

## Browser harness

- Launch system Chrome or bundled Chromium with Playwright.
- `route`: continue only the smoke origin (and `blob:`/`data:`); abort everything else and record hostnames.
- Capture `pageerror` and interesting HTTP statuses (`/upload`, project-document write, `/export`).
- First paint: wait for dashboard controls after locale load — buttons may show translated labels while keys in source stay non-English.

## Sequence (Playwright against loopback origin)

1. **Create** project (New Project control).
2. **Rename** optional — proves title persist path.
3. **Import** fixture via file chooser on Upload control; wait until asset manage control exists.
4. **Timeline** — open asset menu → destination “Timeline” (or drag API if menu absent); assert one timeline clip.
5. **Leave** editor via Back/Home so autosave flush runs.
6. **Reopen** in a **new** browser context; open project by title; assert clip count/name.
7. **Export** — open export UI; set resolution/FPS/codec required by the WBS; start export; save download.
8. **Decode** with lockfile `ffmpeg`/`ffprobe`:
   - video duration within ±1 frame of fixture target
   - width/height/fps/codec as configured
   - audio stream present when expected
   - `ffmpeg -xerror -i out -f null -` succeeds
9. Confirm **source fixture SHA** unchanged.

## Packaged Electron smoke (A-01 class)

Separate from the Playwright HTTP path. Use after an internal directory package exists.

1. Build with the product's **local/dir** package script (no publish channel, no notarize).
2. Prepare two dirs under `execution/<phase>/`:
   - product data dir (SQLite/media)
   - Electron user-data dir (Chromium profile, compositor caches)
3. Launch the binary only with:
   - product data-dir env pointing at the execution data dir
   - `--user-data-dir=<execution user-data dir>`
   - product smoke env flags if present (API/MCP/preload/still-render)
4. Before trusting the run: confirm argv / process cwd show the isolated user-data path. If the process resolves to `~/Library/Application Support/<appname>` (or OS equivalent), kill immediately and fix isolation — packaged prepare may prune versioned compositor bundles in that default profile.
5. Pass only when the product prints its explicit smoke OK marker **and** exits 0. Empty debug logs + early exit without the marker = incomplete evidence.
6. Record codesign `--verify --deep --strict` and Gatekeeper/`spctl` separately. Ad-hoc deep-verify pass + Gatekeeper reject is normal for internal QA and is not ship clearance.

Do not treat packaged smoke as distribution readiness. License disposition still gates public installers.

## Receipt fields

HTTP path: `phase`, `permitted_origin`, `project_id`, `document_write_status`, `clip_count_after_reopen`, `output_sha256`, `output_size_bytes`, `export_engine_badge`, `source_sha256`, `blocked_browser_hostnames`, `browser_page_errors`, `elapsed_seconds`, `http_statuses`.

Packaged path (add): `package_path`, `user_data_dir`, `product_data_dir`, `smoke_marker`, `process_exit_code`, `codesign_verify`, `gatekeeper_assess`.

Store screenshots for reopen + export settings + complete. Keep the MP4 beside `receipt.json` for the HTTP path.

## Fail closed

- Upload 4xx/5xx, missing clip after reopen, export timeout without file, ffprobe mismatch, any `pageerror` during the happy path, or accidental use of host PATH media wrappers without checking real binary identity.
- Packaged launch without isolated `--user-data-dir`, smoke exit non-zero, missing OK marker, or any write under the host default Application Support profile during QA.
