---
name: trend-radar-scraper
description: "Use when scanning daily tech/industry trends, extracting native TikTok WebVTT subtitles and comment insights (Zero-Compute), or fact-checking claims and statistics against primary sources."
version: 2.0.0
author: LinTech Content OS × social-video-intel × firecrawl
license: MIT
metadata:
  hermes:
    tags: [research, trend-radar, tiktok-webvtt, fact-check, anti-hallucination]
    category: research
---

# Radar Quét Trend, Bóc Tách Video Đối Thủ & Kiểm Chứng Sự Thật (`trend-radar-scraper`)

1. **Agent 01 (Research):** Quét xu hướng, trích xuất phụ đề `.vtt` gốc từ TikTok (`__UNIVERSAL_DATA_FOR_REHYDRATION__`), quét 30 bình luận đầu tiên để bắt insight câu hỏi thật của khán giả. Lọc bỏ mọi tin tức có `Actionability_Score < 7`.
2. **Agent 06 (Fact-Check):** Thực thi Sweep 4 (Prove It) & Sweep 5 (Specificity) — đối chiếu mọi số liệu, tên công cụ, API, trích dẫn với nguồn gốc. Tuyệt đối chặn đứng ảo giác (hallucination).
