---
name: video-rendering-engine
description: "Use when rendering video, burning subtitles, or assembling."
version: 1.0.0
author: OPA Engineering
license: MIT
metadata:
  tags: [video, rendering, ffmpeg, libass, subtitles, loudnorm, pipeline]
  hermes:
    tags: [video, rendering, ffmpeg, libass, subtitles, loudnorm, pipeline]
    related_skills: [video-ingestion-pipeline, video-transcription-edit-planning]
---

# Video Rendering Engine, Subtitles & Branding

Production engineering patterns for assembling multi-segment video edits via headless FFmpeg, mathematically mapping subtitles across trimmed clips, burning styled ASS subtitles via `libass`, scaling to 9:16 vertical layouts, and verifying rendered containers.

## When to Use

Use when:
- Assembling multi-segment video clips into an approved cut.
- Burning styled subtitles (`.ass` via `libass`) with exact output timeline synchronization.
- Converting landscape/portrait/square source media into vertical 9:16 layouts without distortion.
- Normalizing multi-segment audio using EBU R128 (`loudnorm`).
- Validating rendered output containers via FFprobe before marking jobs complete.

## Procedure: End-to-End Video Rendering Flow

1. **Verify Approved Edit Plan Gate**:
   - Never initiate rendering without a locked, approved edit plan (`isApproved === true`).
   - Re-verify clip boundaries against source media duration:
     - `clip.start >= 0`
     - `clip.end > clip.start`
     - `clip.end <= sourceDuration + 1.0`
     - No overlapping clips: `clip[i].start >= clip[i-1].end - 0.05`.

2. **Mathematical Subtitle Timeline Mapping**:
   - When trimming and concatenating multiple source segments, source timestamps DO NOT match output timeline timestamps.
   - For each clip $i$ in `clips`, calculate cumulative output offset:
     $$O_i = \sum_{j < i} (clip_j.end - clip_j.start)$$
   - For any transcript segment overlapping $[clip_i.start, clip_i.end]$, compute output start and end:
     $$t_{start}^{out} = O_i + (\max(seg.start, clip_i.start) - clip_i.start)$$
     $$t_{end}^{out} = O_i + (\min(seg.end, clip_i.end) - clip_i.start)$$
   - Format timestamps in ASS specification: `H:MM:SS.cc` (e.g. `0:00:01.50`).

3. **Generate ASS Subtitle File**:
   - Write standard ASS v4.00+ script with 1080x1920 play resolution:
     ```ini
     [Script Info]
     ScriptType: v4.00+
     PlayResX: 1080
     PlayResY: 1920

     [V4+ Styles]
     Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
     Style: Default,Arial,52,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,3,2,2,40,40,260,1
     ```
   - Escape curly braces (`\{`, `\}`) in subtitle dialogue text.

4. **Assemble Safe Non-Shell FFmpeg Filtergraph**:
   - Construct argument array using `child_process.execFile` (never string interpolation in `/bin/sh`):
     - **Multi-clip Trimming & Concat**:
       ```
       [0:v]trim=start=S:end=E,setpts=PTS-STARTPTS[v0];
       [0:a]atrim=start=S:end=E,asetpts=PTS-STARTPTS[a0];
       [v0][a0]...concat=n=N:v=1:a=1[vconcat][aconcat]
       ```
     - **9:16 Scale & Center Crop** (handles landscape, portrait, and square sources without distortion):
       ```
       [vconcat]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[vscaled]
       ```
     - **Subtitle Burn-in via libass**:
       Escape colons and quotes in file path: `path.replace(/:/g, '\\:').replace(/'/g, "\\'")`
       ```
       [vscaled]ass='<escaped_path>'[vsub]
       ```
     - **Audio Normalization** (EBU R128 standard):
       ```
       [aconcat]loudnorm=I=-16:TP=-1.5:LRA=11[anorm]
       ```
     - **Output Encoders**:
       `-c:v libx264 -preset fast -crf 22 -pix_fmt yuv420p -movflags +faststart`

5. **Audio Presence Guard**:
   - Check `hasAudio` from source video probe before assembling audio chains.
   - If `hasAudio === false`: omit all `atrim`, audio concat, `[aconcat]`, `-map [a...]`, and `-c:a aac`. Do not attempt to filter non-existent audio streams.

6. **Post-Render FFprobe Output Verification**:
   - Do NOT mark job completed until output file exists, container is valid, and technical parameters match:
     - `outputWidth === 1080`
     - `outputHeight === 1920`
     - `outputDuration > 0` and within 0.5s of selected clip sum duration
     - `videoCodec === 'h264'`.

7. **Multi-Version Render Retention**:
   - Store render jobs in a versioned table with `UNIQUE(videoId, version)`.
   - When a new version (e.g. v2) fails, mark v2 as `failed`, but keep v1 file on disk and leave `videos.status = 'approved'` if a completed render exists.

---

## Critical Pitfalls & Engineering Rules

1. **Multi-Clip Subtitle Desynchronization**:
   Burning transcript timestamps directly into concatenated video causes subtitles to drift or disappear. You must map source timestamps through cumulative clip duration offsets.
2. **Filter Path Colon Escaping**:
   Passing file paths directly into `ass='...'` fails because FFmpeg interprets colons as filter option delimiters. Always escape colons (`\:`) and single quotes (`\'`).
3. **Audio Stream Discrepancy on Silent Sources**:
   Mapping `[aconcat]` or `-c:a aac` on a video without an audio track causes FFmpeg to exit with error: `Stream map '0:a' matches no streams`. Always branch filtergraph construction on `hasAudio`.
4. **Destructive Video Status Overwrite**:
   Marking `videos.status = 'failed'` when a re-render job fails destroys the record that an earlier version succeeded. Only set `videos.status = 'failed'` if zero completed renders exist for that video.
5. **Subtitle Font Fallback**:
   Non-standard font names without system installation cause libass to drop glyphs or crash. Use universally available fonts (e.g. `Arial`, `Montserrat-Bold`, `Helvetica`) with full Unicode diacritics support.
6. **Parallel Test Runner & Subprocess CPU Contention**:
   When test suites or background workers spawn multiple FFmpeg processes concurrently across parallel runners, CPU thread saturation extends render times from ~1.5s to ~5-6s. Fixed polling loops (e.g. `for (let i = 0; i < 30; i++) { await sleep(200); }` = 6.0s max) prematurely exit and trigger downstream validation errors (e.g. HTTP 422 `render output required`) while FFmpeg is still actively encoding. Always scale polling budgets to at least 12-15s (60+ iterations at 200ms) and cap concurrent FFmpeg workers to `Math.max(1, os.cpus().length - 1)` in production queues.
