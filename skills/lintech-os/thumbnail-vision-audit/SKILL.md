---
name: thumbnail-vision-audit
description: "Use when designing high-CTR 9:16 and 3:4 video thumbnails (Ideogram 3.0, Flux, Gemini Image) for Agent 12 and executing Multimodal Vision QA checks (Vietnamese OCR typo check, TikTok/Reels UI safe-zone verification) for Agent 13."
version: 2.0.0
author: LinTech Content OS × marketingskills/image
license: MIT
metadata:
  hermes:
    tags: [thumbnail, vision-qa, ideogram, flux, safe-zone, ocr, ctr]
    category: creative
---

# Thiết Kế Ảnh Bìa CTR Cao & Kiểm Định Thị Giác (`thumbnail-vision-audit`)

1. **Agent 12 (Thumbnail):** Thiết kế đồng thời `9:16` (`1080x1920`) và `3:4` (`1080x1440`). Chữ trên bìa tối đa 2–5 từ, đặt ở vùng trung tâm `Y: 15% -> 75%`.
2. **Agent 13 (Vision QA):** Quét Multimodal Vision kiểm tra: (a) Chính tả & dấu tiếng Việt OCR 100%, (b) Không phạm vào vùng chết UI TikTok/Reels (`Y > 80%` đáy, `X > 85%` mép phải, `Y < 10%` đỉnh), (c) Điểm tương phản `>= 8.5/10`.
