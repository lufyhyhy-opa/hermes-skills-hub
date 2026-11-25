---
name: dung-video-talking-head
description: Use when có sẵn một video người nói quay dọc 9:16 (HeyGen, avatar AI, quay điện thoại, talking-head) và cần dựng thành video ngắn TikTok/Reels/Shorts có phụ đề động tiếng Việt, chữ hiệu ứng, cắt cỡ cảnh và sound effect — kể cả khi user đưa kèm video mẫu muốn "làm giống", hoặc nói "thêm sub", "dựng video", "kinetic subtitle", "add subtitles and text effects".
triggers:
  - "dựng video talking head"
  - "dung video talking head"
  - "thêm sub vào video"
  - "them sub video"
  - "phụ đề động"
  - "phu de dong"
  - "hiệu ứng chữ"
  - "hieu ung chu video"
  - "edit video HeyGen"
  - "làm giống video mẫu"
  - "kinetic subtitle"
metadata:
  version: 1.1.0
  category: video
  requires: "ffmpeg, node 18+, python 3.10+ (faster-whisper, numpy), font pack D:/MMO/Font/Cinematic fonts pack"
---

# Dựng video talking-head (1.1.0 — router)

`${HERMES_SKILL_DIR}` = thư mục chứa file này. Bản 1.1.0 chạy qua Hermes kanban: mọi việc đi qua **card con trỏ** (P0 → PREP → APPROVE-PREP → INTAKE → PLAN → BUILD → VERIFY → APPROVE-CANARY); operator làm theo `releases/1.1.0/stages/OPERATOR.md`.

## Việc của agent nhận card

1. Lệnh đầu tiên luôn là `python "${HERMES_SKILL_DIR}/releases/1.1.0/scripts/stage.py" STAGE --task ID` — thay `STAGE` bằng chữ sau `STAGE:` của card (card `STAGE: PREP-1` ⇒ `PREP`), `ID` bằng id trong câu "work kanban task t_…", `1.1.0` bằng số sau `RULES: dung-video-talking-head@` của card; không gõ dấu `<` `>`. Ví dụ: `python "${HERMES_SKILL_DIR}/releases/1.1.0/scripts/stage.py" PREP --task t_1a2b3c4d`. Sau đó chỉ chạy đúng lệnh in ở dòng `NEXT`.
2. Chép **nguyên văn** `SUMMARY`/`NEXT` mà script in ra vào comment card bằng tool `kanban_comment`.
3. Không sửa `rules.json`, component hay bất cứ script nào trong `releases/<ver>/`; không tự viết script mới; không dùng `python -c`.
4. Chỉ **PREP** (`releases/<ver>/stages/PREP.md`) và **PLAN** (`releases/<ver>/stages/PLAN.md`) cần agent phán đoán; các stage khác chỉ chạy `stage.py` (riêng VERIFY: xem contact sheet theo dòng `NEXT` — V7).
5. Lỗi hay xong: làm đúng theo dòng `NEXT` — block bằng tool `kanban_block`, complete bằng tool `kanban_complete` chỉ khi `NEXT` bảo; không dùng lệnh `hermes kanban` trong terminal. Card đã bị block thì **không tự unblock**.

## Bản 1.0.0

Card 1.1.0 **không** đọc `legacy/1.0.0/` (quy trình cũ: agent tự viết `edit.json`, tự build/render), không chép gì từ đó.
