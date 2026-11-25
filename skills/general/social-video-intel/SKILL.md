---
name: social-video-intel
description: "Use when extracting and transcribing social video content."
version: 1.0.0
author: OPA Operator
license: MIT
metadata:
  hermes:
    tags: [video, tiktok, transcription, faster-whisper, social-media, content-ops]
---

# Social Video Intelligence

Procedure for ingesting, extracting, and transcribing short-form and social video content when cloud endpoints, standard curl, or scraping tools fail.

---

## 1. TikTok Native Subtitle & Metadata Extraction (Zero-Compute First)

Most TikTok videos carry native ASR/captions. Fetching WebVTT subtitles directly bypasses video downloading, ffmpeg demuxing, and Whisper transcription completely:

### Direct WebVTT & Metadata Scraping
Fetch page HTML with a desktop User-Agent, extract `__UNIVERSAL_DATA_FOR_REHYDRATION__`:

```python
import urllib.request, json, re

req = urllib.request.Request(tiktok_url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode("utf-8", errors="ignore")

m = re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>', html)
if m:
    data = json.loads(m.group(1))
    item = data.get("__DEFAULT_SCOPE__", {}).get("webapp.video-detail", {}).get("itemInfo", {}).get("itemStruct", {})
    subtitles = item.get("video", {}).get("subtitleInfos", [])
    # subtitles[0]["Url"] points directly to .vtt WebVTT caption file
```

### Comment Verification (Resolving ASR Phonetic Ambiguities)
When ASR mishears domain jargon or abbreviations (e.g. "T BA code" -> "T3 Code"), query top comments to disambiguate:

```python
# Video ID from URL or itemStruct["id"]
comment_url = f"https://www.tiktok.com/api/comment/list/?aid=1988&aweme_id={video_id}&count=30"
req = urllib.request.Request(comment_url, headers={
    "User-Agent": "Mozilla/5.0",
    "Referer": tiktok_url
})
with urllib.request.urlopen(req) as resp:
    comments = json.loads(resp.read().decode("utf-8")).get("comments", [])
```

---

## 2. Fallback: Video Extraction via TikWM

```python
import urllib.request, json

url = "https://www.tikwm.com/api/?url=" + target_tiktok_url
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode("utf-8")).get("data", {})

title = data.get("title")
author = data.get("author", {}).get("nickname")
play_url = data.get("play")

if play_url:
    urllib.request.urlretrieve(play_url, "/tmp/video.mp4")
```

---

## 3. Audio Demuxing via ffmpeg

Always convert video to a single-channel 16kHz WAV file before transcription:

```bash
ffmpeg -i /tmp/video.mp4 -vn -ar 16000 -ac 1 /tmp/audio.wav -y
```

---

## 4. Fast Local Speech-to-Text via faster-whisper

Hermes agent venv holds `faster-whisper`:
`/Users/buithiphuongthao/.hermes/hermes-agent/venv/bin/python`

```python
from faster_whisper import WhisperModel

# Use small with int8 compute on CPU for accurate Vietnamese/English inference
model = WhisperModel("small", device="cpu", compute_type="int8")
segments, info = model.transcribe(f"{scratch_dir}/audio.wav", beam_size=5)

for seg in segments:
    print(f"[{seg.start:.2f}s -> {seg.end:.2f}s] {seg.text}")
```

---

## 5. Visual Frame Sampling for On-Screen Artifacts (Infographics, UI, Slides)

Short-form videos compress deep architectures into on-screen graphics while the spoken voice only delivers summaries. Extract frames to analyze visual artifacts:

```bash
# Sample 1 frame every 3 seconds (0.33 fps)
mkdir -p "$SCRATCH_DIR/frames"
ffmpeg -i "$SCRATCH_DIR/video.mp4" -vf "fps=1/3" "$SCRATCH_DIR/frames/frame_%03d.jpg" -y
```

### Visual Pitfalls & Rules
- **Crop dense diagrams before vision call**: Full vertical 9:16 frames (576x1024) downscale small node text during vision analysis. Crop into 3 horizontal slices (top 0–38%, middle 35–72%, bottom 70–100%) to preserve full native pixel resolution for OCR/reading.
- **Triage talking-head vs slide frames**: Check frame sequence to distinguish presenter-only frames from graphic/dashboard frames.

---

## 6. Pipeline Integration & Synthesis

After obtaining transcripts and visual frame data:
1. **Hook Analysis (0-3s)**: Isolate the opening sentence; verify if it states problem or core outcome directly.
2. **Visual Flow Reconciliation**: Match spoken timestamps to on-screen stages/nodes.
3. **Architecture Mapping**: Extract complete agent roles, gate criteria (e.g. human approval points, score thresholds), and closed-loop learning loops.
