---
name: video-transcription-edit-planning
description: "Use when transcribing video or creating AI edit plans."
version: 1.0.0
author: OPA Engineering
license: MIT
metadata:
  tags: [video, transcription, whisper, edit-plan, llm, silence, pipeline]
  hermes:
    tags: [video, transcription, whisper, edit-plan, llm, silence, pipeline]
    related_skills: [video-ingestion-pipeline, video-rendering-engine]
---

# Video Transcription & AI Edit Planning

Production engineering patterns for extracting audio, transcribing speech with word-level timestamps, validating transcript boundaries, enforcing optimistic concurrency control, and generating silence-aware AI edit plans in automated short-form video SaaS platforms.

## Procedure: Transcription & Edit Planning Flow

1. **Audio Extraction for Transcription**:
   - Do not send high-bitrate video containers directly to transcription providers.
   - Extract uncompressed 16kHz mono PCM audio via FFmpeg:
     ```bash
     ffmpeg -y -i input.mp4 -vn -ar 16000 -ac 1 -c:a pcm_s16le audio.wav
     ```
   - Reduces network payload by >90% and eliminates container decode failures in Whisper.

2. **Transcription Invocation & Caching**:
   - Pass extracted audio to speech-to-text provider (OpenAI Whisper or deterministic test fake).
   - Enforce idempotency: if a valid transcript already exists for the video version and `force !== true`, return the cached transcript without incurring paid model calls.

3. **Transcript Segment Validation**:
   - Enforce segment constraints:
     - `start >= 0`
     - `end > start`
     - Chronological sorting: `seg[i].start >= seg[i-1].start`
     - Non-empty text.
   - Handle audio drift: if trailing segment end slightly exceeds video stream PTS duration, clamp `end = Math.min(end, videoDuration)` when `start < videoDuration`.

4. **Optimistic Concurrency Control (OCC) on Edits**:
   - Store an integer `version` field on transcript records.
   - On `PATCH` updates, verify client `version === current.version`.
   - Reject mismatches with HTTP `409 Conflict` to prevent silent lost updates when multiple users edit concurrently. Increment `version` on success.

5. **Silence-Aware AI Edit Planning**:
   - Combine detected silence intervals (`>=0.6s`) with transcript segments.
   - Filter out clip segments falling squarely inside detected dead air, while preserving natural breath pauses.
   - Prompt LLM with video technical constraints (`durationSeconds`, `width`, `height`, `fps`), brand tone, and content goals.
   - Require structured JSON output containing: `hookText`, `clips` (`start`, `end`, `text`, `reason`), `subtitleStyle`.

6. **Server-Side Plan Validation & Approval**:
   - Validate proposed clips:
     - No overlapping clips (`clip[i].start >= clip[i-1].end - 0.05`).
     - Every clip within `[0, videoDuration + 0.5]`.
     - Total duration > 0 and within target duration ceiling.
   - Validate subtitle style against allowlisted fonts (`Montserrat-Bold`, `Inter`, `Plus Jakarta Sans`).
   - On approval (`POST /api/v1/videos/:id/edit-plan/approve`), mark `isApproved = true`, record `approvedAt`, and transition video state to `ready_for_review`. Lock approved plan against further mutation.

---

## Critical Pitfalls & Engineering Rules

1. **Whisper Trailing Boundary Drift**:
   Speech recognition models frequently produce timestamps slightly past the video container PTS. Never reject an entire transcript for fractional trailing drift; clamp `end` to media duration if `start` is within bounds.
2. **Stale Overwrite Prevention**:
   Always require and verify integer revision versions (`version`) on transcript and edit plan updates. Never allow unversioned PATCH requests to overwrite human-reviewed text.
3. **Prompt Injection Defense in Transcripts**:
   Treat transcript text and user instructions as untrusted user data. Enforce strict JSON schema validation on the LLM response; never execute raw LLM text or shell commands.
4. **Silence as Supporting Evidence**:
   Do not blindly remove every silence interval. Treat silence detection as supporting evidence to eliminate dead air (>0.6s) while keeping natural dramatic pauses in talking-head content.
