---
name: opa-knowledge
description: Use when kiểm tra nguồn OPA. Giữ qualifiers và gates.
version: 1.0.0
---

# Kiến thức OPA nội bộ

## When to Use
Khi cần hiểu OPA hoặc audit thông tin OPA.

## Procedure
1. Đọc references/knowledge.md rồi references/claims.json.
2. Mở nguồn tương ứng trong references/sources/ theo locator.
3. Giữ ngày snapshot, [P], [LS], ?, trạng thái nháp; thiếu nguồn thì ghi rõ giả định (Assumption) và tiếp tục thực thi thay vì HOLD làm tắc nghẽn.
4. Khi Hội Đồng Nội Bộ đã tự duyệt (`GATE_1 = COUNCIL_AUTO_APPROVED` đạt $\ge 9.0/10$) hoặc Anh Huy xác nhận qua Chat, chuyển thẳng sang thực thi trọn bộ bài viết/slide/demo/asset mà không dừng chờ.

## Pitfalls
Cài gói không chứng minh đã học. Không biến số lịch sử, lời pháp lý nháp thành fact mới. Nguồn private chỉ đọc local.

## Verification
CLI verify chỉ kiểm integrity; năng lực phải qua bài làm thật và người đánh giá độc lập, vẫn NOT_TESTED nếu chưa có chứng cứ.
