---
name: ghosttrack-osint
description: "OSINT & Digital Footprint Reconnaissance Web Dashboard and API (mintisan/GhostTrackWeb). Tracks IP geolocation/ASN/ISP, international phone number carrier/region/timezone, social media username presence across 18+ platforms, and public IP. Runs persistently at http://127.0.0.1:8192."
version: 2.0.0
author: mintisan / HunxByts (Integrated for Hermes Agent & LinTech OS)
license: MIT
platforms: [macos, linux, windows]
metadata:
  tags: [osint, ghosttrack, ip-tracker, phone-tracker, username-tracker, recon, research]
  hermes:
    tags: [GhostTrack, OSINT, IPTracker, PhoneTracker, UsernameRecon]
    related_skills: [research]
---

# GhostTrackWeb OSINT Dashboard & API (`mintisan/GhostTrackWeb`)

- **Web Dashboard URL:** `http://localhost:8192` (hoặc tab **`🕵️ GhostTrack OSINT`** ngay trong **Hermes Desktop → Văn Phòng 3D**)
- **Thư mục cài đặt:** `/Users/buithiphuongthao/.hermes/ghosttrack-web`
- **LaunchAgent chạy ngầm 24/7:** `/Users/buithiphuongthao/Library/LaunchAgents/ai.hermes.ghosttrack-web.plist`

## 1. Các trang trên Web Dashboard (`http://localhost:8192`)
- **Trang chủ (`/`)**: Tổng quan 4 công cụ OSINT (hỗ trợ chuyển đổi **Dark Mode 🌙 / Light Mode ☀️** góc trên bên phải).
- **IP Tracker (`/ip-tracker`)**: Tra cứu vị trí địa lý, ISP, ASN, Múi giờ, Tọa độ và mở trực tiếp Google Maps của địa chỉ IP.
- **Phone Tracker (`/phone-tracker`)**: Tra cứu nhà mạng (Carrier), quốc gia, định dạng chuẩn E.164/Quốc tế của số điện thoại (nhập dạng `+<mã_quốc_gia><số>`, ví dụ `+84912345678`).
- **Username Tracker (`/username-tracker`)**: Quét song song đa luồng sự tồn tại của một `username` trên 18 mạng xã hội lớn (Facebook, Twitter/X, Instagram, LinkedIn, GitHub, TikTok, YouTube, Telegram, Medium, Behance, Dribbble, Twitch...).
- **My IP (`/my-ip`)**: Hiển thị địa chỉ Public IP hiện tại của thiết bị.

## 2. Gọi nhanh qua API cho Agent (`agent-01-research`)
1. **Tra cứu IP (`POST /api/track-ip`)**:
   ```bash
   curl -s -X POST http://127.0.0.1:8192/api/track-ip -H "Content-Type: application/json" -d '{"ip_address":"8.8.8.8"}'
   ```
2. **Tra cứu Số điện thoại (`POST /api/track-phone`)**:
   ```bash
   curl -s -X POST http://127.0.0.1:8192/api/track-phone -H "Content-Type: application/json" -d '{"phone_number":"+84912345678"}'
   ```
3. **Tra cứu Username trên 18 MXH (`POST /api/track-username`)**:
   ```bash
   curl -s -X POST http://127.0.0.1:8192/api/track-username -H "Content-Type: application/json" -d '{"username":"torvalds"}'
   ```
4. **Kiểm tra Public IP (`GET /api/my-ip`)**:
   ```bash
   curl -s http://127.0.0.1:8192/api/my-ip
   ```
