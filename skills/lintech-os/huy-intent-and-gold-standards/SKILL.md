---
name: huy-intent-and-gold-standards
description: "Bộ Giải Mã Ý Định Ngầm (Nói 1 Hiểu 10) và Kho Mẫu Chuẩn Vàng 10/10 (Few-Shot Gold Standards) dành riêng cho Anh Huy (Huy × OPA / LinTech OS). Nạp kỹ năng này khi cần hiểu sâu ý định từ câu lệnh ngắn, lập kế hoạch GTM, viết nội dung thương hiệu cá nhân, làm Slide thuyết trình hoặc thiết kế Web Demo."
version: 1.0.0
author: LinTech Autonomous Council
license: MIT
metadata:
  hermes:
    tags: [intent-decoder, gold-standards, few-shot, brand-voice, anh-huy, opa, zero-babysitting]
    category: lintech-os
---

# 🧠 Bộ Giải Mã Ý Định Ngầm & Kho Mẫu Chuẩn 10/10 Của Anh Huy (`huy-intent-and-gold-standards`)

## 1. Ma Trận Giải Mã Ý Định Ngầm ("Nói 1 Hiểu 10" — Implicit Intent Decoder)

Anh Huy là người điều hành bận rộn, thường đưa ra mệnh lệnh ngắn gọn, viết tắt hoặc chỉ nêu mục tiêu tổng quát. **CẤM hỏi lại các câu hình thức** — hãy tự động dịch câu lệnh ngắn của Anh Huy sang **Chuỗi Thành Phẩm Hoàn Chỉnh (End-to-End Deliverable Package)** theo bảng sau:

| Câu lệnh ngắn của Anh Huy | Ý định thực sự đằng sau (End-Goal) | Hành động tự động bắt buộc của Dàn Agent |
|---|---|---|
| *"Lên kế hoạch / chiến lược X"* | Cần một bộ kế hoạch thực chiến có thể đem đi triển khai hoặc gửi đối tác ngay hôm nay | 1. `agent-01` quét số liệu & đối thủ<br>2. `agent-02` lập 3 phương án đối lập (Tree of Thoughts)<br>3. `agent-05` + `agent-06` phản biện Red-Team, tự nâng cấp lên bản `v2/v3` ($\ge 9.0/10$)<br>4. Xuất trọn bộ: **Tài liệu Master Plan (.md) + Bảng phân bổ WBS (.csv) + Bài viết/Kịch bản mẫu** |
| *"Làm slide / pitch deck / gửi đối tác X"* | Cần bộ slide chuẩn McKinsey thuyết phục đối tác bằng con số & giao diện đẳng cấp | 1. Nạp `autonomous-slide-council`<br>2. Lên khung SCQA (1 slide = 1 kết luận có số liệu, tối đa 30 từ/slide)<br>3. Xuất **đồng thời cả 2 định dạng**: File **Web Slide HTML tương tác `16:9`** (điều hướng phím mũi tên) VÀ file **PowerPoint `.pptx`**<br>4. Chạy `/Users/buithiphuongthao/.local/bin/hermes-verify-harness` để xác thực 0% lỗi cắt cụt/template |
| *"Làm web / giao diện / demo X"* | Cần một trang web sống động, thẩm mỹ cao, không mùi template AI rẻ tiền, chạy được ngay | 1. `agent-18` định hình Design Tokens (Editorial / Precision Dark Tech / Area Design System)<br>2. `agent-17` code giao diện hoàn chỉnh, cấm `useEffect` bừa bãi, cấm comment cắt cụt (`// ... rest of code`)<br>3. Chạy `/Users/buithiphuongthao/.local/bin/hermes-verify-harness` (hoặc `npm run verify`) xuất `trust_pyramid_receipt.json` |
| *"Viết bài / chuỗi bài về X"* | Cần bài viết sắc bén, đọc như chuyên gia thật đang trò chuyện, có Hook giữ chân trong 1.5s | 1. `agent-03` lập dàn ý 1-3-1 gắn dẫn chứng thật<br>2. `agent-04` viết bài 0% mùi AI<br>3. `agent-05` chấm điểm $\ge 8.5/10$ (nếu chưa đạt thì tự phẫu thuật câu chữ tại chỗ)<br>4. `agent-07` + `agent-08` nhân bản luôn sang Threads & Carousel + chạy `hermes-verify-harness` quét sạch từ cấm AI Slop |
| Gõ nhanh / viết tắt / sai chính tả nhẹ (VD: `"Agele 2"`, `"ok"`, `"làm đi"`, `"duyệt"`) | Lệnh xác nhận chính thức (`PLAN_APPROVED`) | Khớp ngay với phương án/ngữ cảnh gần nhất (`Angle_2`) và kích hoạt toàn bộ nhánh thực thi ngay lập tức |

---

## 2. Đối Chiếu Trực Tiếp: ❌ Văn Mẫu AI (Bị Loại) vs ✅ Chuẩn Giọng Anh Huy (10/10)

### 2.1. Mở bài (Hook 2 dòng đầu)
- ❌ **Bản AI Slop (0 điểm — Bị loại ngay):**
  > *"Trong kỷ nguyên số bùng nổ hiện nay, AI không chỉ là một công cụ mà còn là chìa khóa vàng giúp doanh nghiệp tối ưu hóa hiệu suất. Hãy cùng khám phá bí mật đằng sau hệ thống 18 Agent!"*
- ✅ **Bản Chuẩn Giọng Anh Huy (10/10 — Trực diện, có con số & nỗi đau thật):**
  > *"Tuần trước mình cắt toàn bộ 4 tiếng ngồi viết content mỗi ngày xuống còn đúng 12 phút duyệt bài cuối. Bí quyết nằm ở việc tách riêng con AI viết bài và con AI chuyên đi bắt lỗi."*

### 2.2. Thân bài (Giải thích cơ chế & Unit Economics)
- ❌ **Bản AI Slop (Lan man, tính từ cảm tính):**
  > *"Hệ thống này cực kỳ thông minh và mang lại hiệu quả vượt trội. Nó giúp bạn tiết kiệm rất nhiều thời gian, không cần biết code, không tốn chi phí, không mất công sức."*
- ✅ **Bản Chuẩn Giọng Anh Huy (10/10 — Cơ chế cụ thể, nhịp 1-3-1):**
  > *"Sai lầm của 90% người dùng ChatGPT là bắt 1 cửa sổ chat vừa nghiên cứu, vừa viết bài, vừa tự khen bài nó viết.*
  > *Trong hệ thống của mình, `agent-04` chỉ được phép viết nháp. Ngay sau đó, `agent-05` nhảy vào chấm điểm theo 7 tiêu chí và thẳng tay gạch bỏ mọi câu sáo rỗng. Bản thảo nào dưới 8.5 điểm bị trả về viết lại ngay trong nội bộ.*
  > *Khi bài đến tay mình, nó đã là bản v3 sạch bóng văn mẫu."*

### 2.3. Lập Kế Hoạch Kinh Doanh / GTM (Chuẩn Thực Chiến)
- **Mọi bản kế hoạch trình Anh Huy BẮT BUỘC phải có:**
  1. **Bảng Unit Economics & Ràng buộc thực tế:** Ngân sách (VD: 10–30 triệu VNĐ/tháng ưu tiên organic/partner), CAC mục tiêu, LTV, tỷ lệ chuyển đổi từng tầng phễu (TOFU $\rightarrow$ MOFU $\rightarrow$ BOFU).
  2. **3 Phương Án Bất Đối Xứng (Tree of Thoughts):** Kèm bảng so sánh ưu/nhược điểm và lý do Hội đồng chọn phương án chiến thắng (`Recommended Winner`).
  3. **Biên bản Phản Biện Red-Team:** Liệt kê rõ 5 lỗ hổng của bản v1 và cách bản v2/v3 đã vá triệt để các lỗ hổng đó như thế nào.
  4. **Bảng Phân Rã Công Việc (WBS / Action Plan):** Ai làm gì, theo tuần/ngày, KPI đầu ra đo đếm được.
