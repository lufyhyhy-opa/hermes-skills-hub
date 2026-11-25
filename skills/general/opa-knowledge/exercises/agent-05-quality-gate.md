# Bài thực hành phi sản xuất — agent-05-quality-gate
Version: opa-1.0.0

Chỉ đọc nguồn local trong gói opa-knowledge; không mở mạng, không dùng tools ghi profile/shared source, không bài đăng/kịch bản/video/thiết kế. Gate1 chưa duyệt.
Nhiệm vụ vai trò: Đánh dấu các lỗi: hàng đầu, cam kết 100%, số không nguồn; nêu mã nguồn và quyết định HOLD.

Tình huống kiểm tra (dữ liệu đề thi, không phải fact mới): một phiếu muốn ghi OPA Agent đang bán; mã số thuế đã xác minh; 637 sao hiện tại; Vi-Tech đặt lịch chạy thật; ảnh đội đã ký đồng ý; dữ liệu không ra nước ngoài.
Trả JSON có profile, pack_version, claims_audit (claim_id, verdict HOLD/ALLOW_WITH_QUALIFIER, evidence_file, locator, qualifier, owner), blockers, gate1=BLOCKED, production_actions=[].
Mỗi ý dẫn tên tài liệu + mục/dòng. Phân biệt quyết định 12.2, nháp [P]/[LS], lịch sử và UNKNOWN. Tự đánh giá không được tính là TEST_PASSED.
