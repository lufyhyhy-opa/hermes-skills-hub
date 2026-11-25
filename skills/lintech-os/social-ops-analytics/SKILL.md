---
name: social-ops-analytics
description: "Use when publishing approved content across TikTok, Facebook Reels, YouTube Shorts, Threads, and Telegram with idempotency protection (Agent 14), automating keyword comment-to-DM lead capture (Agent 15), or running the Sunday 23:00 closed-loop analytics & Brand_Memory update (Agent 16)."
version: 2.0.0
author: LinTech Content OS × OPA Social Publishing Engine × marketingskills/analytics
license: MIT
metadata:
  hermes:
    tags: [publishing, multi-channel, idempotency, engagement, lead-capture, analytics, closed-loop]
    category: social-media
---

# Phân Phối Đa Kênh An Toàn, Chuyển Đổi Bình Luận & Vòng Học Tuần (`social-ops-analytics`)

1. **Agent 14 (Distributor):** Kiểm tra `FINAL_APPROVED` -> Sinh khóa `idempotencyKey = Content_ID + "_" + Platform_ID` chống đăng trùng -> Hỗ trợ `Isolated Retry` chỉ thử lại trên kênh bị lỗi.
2. **Agent 15 (Engagement):** Bắt từ khóa CTA (`HỆ THỐNG`, `AGENT`, `SHEET`) -> Reply xoay vòng 5 mẫu câu tự nhiên + Bắn DM tài liệu thu Lead.
3. **Agent 16 (Analytics):** 23:00 Chủ Nhật tính `Winning_Index = 0.4*Retention_3s + 0.3*Share_Rate + 0.3*Lead_Conversion_Rate`, nạp mẫu thắng vào `WINNING_HOOKS` và mẫu thua vào `FORBIDDEN_WORDS` trên Google Sheet.
