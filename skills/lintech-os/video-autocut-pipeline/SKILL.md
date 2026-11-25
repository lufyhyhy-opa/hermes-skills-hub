---
name: video-autocut-pipeline
description: "Use when processing raw talking-head video clips into vertical 9:16 short-form videos: 16kHz audio demuxing, Faster-Whisper word-level transcription, VAD silence removal (>0.4s), mathematical ASS subtitle timeline mapping, EBU R128 (-14 LUFS) audio leveling, and FFprobe QA verification."
version: 2.0.0
author: LinTech Content OS × OPA Video Rendering Engine × Auto-Editor
license: MIT
metadata:
  hermes:
    tags: [video-editing, ffmpeg, faster-whisper, auto-editor, libass, kinetic-subtitles, video-qa]
    category: media
---

# Dây Chuyền Hậu Kỳ Video Tự Động & Kiểm Định Kỹ Thuật (`video-autocut-pipeline`)

1. **Agent 10 (Video Editor):** Tách WAV 16kHz -> Chạy `faster-whisper` (`word_timestamps=True`, `vad_filter=True`) -> Cắt khoảng lặng `>0.4s` -> Tính độ dời tích lũy $O_i$ để ánh xạ phụ đề `.ass` khớp từng mili-giây -> Chuẩn hóa âm thanh `loudnorm=I=-14:TP=-1.5:LRA=11` và xuất `1080x1920` H.264.
2. **Agent 11 (Video QA):** Dùng `ffprobe` xác minh `30.0 <= duration <= 59.9s`, độ phân giải `1080x1920`, không lệch phụ đề quá `100ms`.
