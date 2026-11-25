---
name: remotion-kinetic-overlays
description: "Unified Remotion library for Short-Form Kinetic Typography, Word-Level Animated Captions (13 themes including Hormozi/Hustle, MrBeast, Karaoke, Kinetic, Pop), and B-Roll Cutaway Overlay Primitives (TitleOverlay, Comparison, ListReveal, Flow, Safe-Area Guard)."
version: 1.0.0
author: LinTech Content OS (vshukla7/remotion-captions-themes × diegolopezislas13-jpg/remotion-kinetic-kit × alichherawalla/video-overlay-kit)
license: MIT
metadata:
  hermes:
    tags: [remotion, kinetic-typography, captions, subtitles, b-roll-overlay, shorts, reels, tiktok]
    category: media
---

# Remotion Kinetic Captions, Text Kits & B-Roll Overlay Primitives (`remotion-kinetic-overlays`)

Bộ thư viện hợp nhất 3 kho mã nguồn mở tốt nhất trên GitHub cho **Agent 09 (Scriptwriter)** và **Agent 10 (Video Editor)** khi sản xuất video ngắn `9:16` (`1080x1920`).

---

## 1. Cấu Trúc Thư Mục Trong Skill (`${HERMES_SKILL_DIR}`)

1. **`${HERMES_SKILL_DIR}/captions-themes/src/themes/`** *(từ `vshukla7/remotion-captions-themes`)*:
   - **13 Theme Phụ Đề Động Mức Từ (Word-Level Kinetic Captions):**
     - `hustle.tsx`: Phong cách **Alex Hormozi** (chữ in hoa đậm, từ đang nói đổi màu Vàng `#FFD700` / Xanh lá kèm phóng nhẹ).
     - `beast.tsx`: Phong cách **MrBeast** (chữ bật nảy mạnh từng cụm ngắn, viền đen dày).
     - `karaoke.tsx`: Tô màu trượt mượt theo từng âm tiết đang phát âm.
     - `kinetic-01.tsx` & `kinetic-02.tsx`: Chữ động trượt và xoay theo nhịp nhanh.
     - `pop.tsx` & `poppin.tsx`: Hiệu ứng nảy lò xo (Spring Pop) cho từng từ khóa nhấn.
     - `podcast.tsx`, `soft-ai.tsx`, `simple-one-word.tsx`, `grape.tsx`, `gaming-stream.tsx`, `aarit.tsx`.
   - **Layout Engine (`captions-themes/src/layout/`):** Tự động tính toán vị trí neo (`anchors.ts`), chống đè chữ (`collision.ts`) và quy đổi dấu thời gian từ sang khung hình (`secondsToFrames.ts`, `useWordTiming.ts`).

2. **`${HERMES_SKILL_DIR}/kinetic-kit/src/`** *(từ `diegolopezislas13-jpg/remotion-kinetic-kit`)*:
   - Các khối cảnh (Scene Primitives) dựng sẵn cho Reels/TikTok:
     - **Spring Blur/Scale Entrance:** Chữ tiêu đề 3 giây đầu (`3s Hook`) lao vào khung hình có độ mờ chuyển động (motion blur) và độ nảy lò xo.
     - **Flash Cut & Light-Sweep Transitions:** Chuyển cảnh chớp sáng và vệt sáng quét qua chữ tiêu đề.
     - **Hook Cards / Pain-Point Cards / Benefit Cards.**

3. **`${HERMES_SKILL_DIR}/overlay-kit/src/`** *(từ `alichherawalla/video-overlay-kit` + MCP Server tại `overlay-kit/mcp/`)*:
   - Các Component đè lên cảnh A-roll hoặc B-roll:
     - `components/TitleOverlay.tsx`: Tiêu đề nổi đầu video hoặc chuyển chương.
     - `components/Comparison.tsx`: Bảng so sánh đối lập Trước / Sau (Old Way ❌ vs. New Way ✅).
     - `components/ListReveal.tsx`: Danh sách bật ra từng dòng khớp với từng ý người nói đang đọc.
     - `components/Flow.tsx`: Sơ đồ quy trình từng bước (Flowchart động) thay thế cho ảnh tĩnh nhàm chán.
     - `scene/safearea.ts`: Tự động khóa vùng an toàn `9:16` để không bị giao diện TikTok/Reels/Shorts che khuất.

---

## 2. Quy Tắc Phối Hợp Giữa `agent-09`, `agent-10` và `agent-11`

- **Trong kịch bản của `agent-09-scriptwriter` (`editor_cue`):**
  - Chỉ định rõ `layout_mode`: `a-roll` | `punch` | `split` (nửa trên B-roll/Receipt, nửa dưới người nói) | `b-roll` (toàn màn hình).
  - Chỉ định rõ `broll_type`: `receipt` (bài báo/tweet/trang web thật) | `entity` (công cụ/nhân vật) | `concept` (`Comparison` / `ListReveal` / `Flow`).
  - Chỉ định rõ `caption_theme`: mặc định dùng `hustle` (Hormozi) hoặc `kinetic-01`.
- **Khi `agent-10-video-editor` dựng video:**
  - Luôn đặt cảnh B-roll rơi **đúng vào từ khóa đang được nói (`+0.2s lead`)**, kéo dài `2.0s – 3.5s`.
  - Nếu 2 cảnh B-roll cách nhau dưới nửa câu (`< 1.0s`), nối liền 2 cảnh B-roll lại để tránh nháy mặt người nói `< 1s` gây lỗi thị giác.
