---
name: gsheet-control-plane
description: "Use when reading or updating the LinTech Content OS Google Sheet Control Plane (Brand_Memory, Content_Pipeline, Performance_KPI) or synchronizing product-marketing context across all 16 agents."
version: 2.0.0
author: LinTech Content OS
license: MIT
metadata:
  hermes:
    tags: [google-sheet, control-plane, brand-memory, database, pipeline]
    category: productivity
---

# Google Sheet Control Plane & Brand Brain (`gsheet-control-plane`)

Quản lý 3 bảng điều khiển trung tâm của LinTech Content OS (`Brand_Memory`, `Content_Pipeline`, `Performance_KPI`).

## Xác minh backend trước khi đồng bộ
1. Đọc script trước lần sử dụng đầu tiên; xác định nơi lưu và side effect của cả thao tác đọc. Không suy từ tên skill hay dòng `[OK]` rằng đã gọi Google Sheets.
2. Implementation dùng `local_db` và `json.dump` chỉ lưu JSON cục bộ. `read_memory` có thể khởi tạo file với Brand_Memory mẫu; không trình dữ liệu mẫu là bộ nhớ thương hiệu đã được người dùng xác nhận.
3. Kiểm tra nơi ghi thuộc profile đang hoạt động. Nếu script ghi đường dẫn dùng chung ngoài profile, dừng để sửa qua quy trình được phép hoặc dùng artefact tách biệt trong workspace; không làm lẫn trạng thái giữa các profile.
4. Chỉ báo Google Sheet đã đồng bộ sau khi ghi backend thật và đọc lại đúng spreadsheet, tab, Content_ID. Nếu chỉ lưu nội bộ, ghi `local_only` và `google_sheet_synced: false`, không gọi đó là đồng bộ Sheet.
5. Tách quyết định tại chat, biên nhận Telegram, phiên bản artefact, QA, số vòng sửa và quyền phát hành. Dùng `telegram-hitl-gate` cho chuyển cổng; agent hoàn thành không đồng nghĩa `PLAN_APPROVED` hay `FINAL_APPROVED`.
6. Kiểm tra semantics cập nhật: `update_status` hiện thay cả record của Content_ID. Bảo toàn trường cần thiết bằng merge đã kiểm chứng, không giả định script giữ nguyên lịch sử.
7. Thiếu credential/spreadsheet_id thì fail closed (exit 2). Không fallback JSON mẫu, không gọi UNIT_TEST/fixture là đồng bộ live. Adapter staged trong workspace chưa thay script profile cho đến khi đọc lại đúng spreadsheet/tab/key.
8. Vòng đời bắt buộc, không nhảy cóc, không đổi thành chuỗi rút gọn kiểu DRAFT→PLAN_PENDING: `RAW_SIGNAL` → `RESEARCHED` → `PLAN_PROPOSED` → `PLAN_APPROVED`, rồi nhánh độc lập trong `Branch_States` (copy: `OUTLINED`→`DRAFTED`→`COPY_QA_PASSED`→`FACT_VERIFIED` rồi cả `REPURPOSED_THREADS` và `CAROUSEL_READY`; video: `SCRIPT_READY`→`WAITING_RAW_VIDEO`→`RAW_FOOTAGE_UPLOADED`→`VIDEO_RENDERED` rồi cả `VIDEO_QA_PASSED` và `THUMB_GENERATED`→`VISION_QA_PASSED`; web tùy chọn: `BRAND_TOKENS_SPECIFIED`→`WEB_UI_IMPLEMENTED`). `Status` đơn không được ngụ ý nhánh đã xong. Gom `PACKAGE_ASSEMBLED` chỉ khi đủ nút nhánh bắt buộc và đúng bốn chứng chỉ `COPY_QA_PASSED`, `FACT_VERIFIED`, `VIDEO_QA_PASSED`, `VISION_QA_PASSED` gắn phiên bản; rồi `FINAL_APPROVED` → `PUBLISHED_OMNICHANNEL` → `ENGAGEMENT_ACTIVE` → `WEEKLY_ANALYZED`.
9. Không để adapter tự ghi `HITL_Receipts`. Ô `Verified=TRUE` do agent ghi không phải duyệt người. Thiếu verifier độc lập thì chặn mọi ghi từ `PLAN_APPROVED` trở đi.

## Lệnh thực thi Script
- Đọc Brand Memory: `python3 "${HERMES_SKILL_DIR}/scripts/gsheet_sync.py" --action read_memory`
- Cập nhật trạng thái bài: `python3 "${HERMES_SKILL_DIR}/scripts/gsheet_sync.py" --action update_status --content-id "CNT_001" --status "PLAN_APPROVED"`
- Cập nhật quy luật học tuần: `python3 "${HERMES_SKILL_DIR}/scripts/gsheet_sync.py" --action upsert_memory --key "WINNING_HOOKS" --value "..." --agent "agent-16-analytics"`
