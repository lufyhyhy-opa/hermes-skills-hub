---
name: telegram-hitl-gate
description: "Use when dispatching Human-in-the-Loop approval cards to Telegram Bot for Gate 1 (Plan Approval), Gate 2 (Raw Video Shooting Sheet), and Gate 3 (Final Multi-Channel Release Gate)."
version: 2.0.0
author: LinTech Content OS
license: MIT
metadata:
  hermes:
    tags: [telegram, human-in-the-loop, approval-gate, inline-keyboard, orchestrator]
    category: productivity
---

# Trạm Duyệt Con Người (`telegram-hitl-gate`) — Tương Thích Zero-Babysitting

> **QUY TẮC ƯU TIÊN TỐI CAO (ZERO-BABYSITTING OVERRIDE):**
> - **Cổng 1 (`gate_1_plan`):** Mặc định được **Hội Đồng Nội Bộ tự duyệt (`COUNCIL_AUTO_APPROVED`)** sau khi nâng cấp v1 $\rightarrow$ v2/v3 đạt $\ge 9.0/10$, hoặc nhận chỉ đạo trực tiếp của Anh Huy trên cửa sổ Chat. **TUYỆT ĐỐI KHÔNG chặn pipeline ở Cổng 1 vì thiếu Telegram token hay thiếu nút bấm Telegram.**
> - **Cổng 2 (`gate_2_shoot`):** Chỉ áp dụng riêng cho nhánh dựng video cần cảnh quay mặt thật (`agent-10`). Mọi nhánh khác (Kế hoạch, Bài viết, Slide thuyết trình, Ảnh bìa, Web Demo) phải chạy xuyên suốt 100% không dừng ở Cổng 2.
> - **Cổng 3 (`gate_3_publish`):** Chỉ dùng để xác nhận cuối trước khi gọi API đăng bài thật lên mạng xã hội công khai (`agent-14`).

Gửi phiếu duyệt qua Telegram Bot (khi đã cấu hình Telegram và chỉ khi cần thiết ở Cổng 3):
Lệnh gọi: `python3 "${HERMES_SKILL_DIR}/scripts/telegram_gate.py" --gate gate_3_publish --content-id CNT_001 --message-file /tmp/msg.txt`
