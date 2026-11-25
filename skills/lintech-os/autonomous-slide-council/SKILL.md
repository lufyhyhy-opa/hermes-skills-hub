---
name: autonomous-slide-council
description: "Hội đồng 4 Agent tự động họp, phản biện kịch bản McKinsey SCQA và xuất Slide thuyết trình hoàn chỉnh (.html tương tác 16:9 & .pptx) không cần con người sửa lỗi thủ công."
version: 1.0.0
author: LinTech Content OS
license: MIT
metadata:
  hermes:
    tags: [presentation, slide-deck, pptx, html-slides, mckinsey, storytelling, autonomous-council]
    category: creative
    related_skills: [personal-os-operations, marketing-council, popular-web-designs, claude-design]
---

# Autonomous Slide Council (Hội Đồng Tự Động Thiết Kế & Xuất Slide Thuyết Trình)

Sử dụng kỹ năng này bấtất cứ khi nào người dùng yêu cầu **tạo slide thuyết trình, pitch deck, partner deck, báo cáo chiến lược, hoặc chuyển tài liệu thành bản trình chiếu**.

## Nguyên Tắc Cốt Lõi: Zero-Babysitting (Tự Họp – Tự Sửa – Tự Xuất File)
Tuyệt đối **KHÔNG** trả về một dàn ý sơ sài rồi hỏi *"Anh có muốn em làm tiếp không?"*.
Bạn phải tự động điều phối **Hội Đồng 4 Vai (4-Agent Internal Council)** chạy một mạch từ ý tưởng đến khi xuất ra **file Slide hoàn chỉnh (`.html` + `.pptx`)**:

---

## Quy Trình 4 Pha Tự Trị Khép Kín

### Pha 1: Chiến Lược & Dòng Chảy Câu Chuyện (`McKinsey Strategist` — `agent-02-plan`)
1. Áp dụng khung **SCQA (Situation – Complication – Question – Answer)** và **Pyramid Principle**.
2. Sinh ra **3 hướng tiếp cận kịch bản (3 Narrative Angles)**, tự so sánh và chọn ra cấu trúc sắc bén nhất.
3. Thiết kế cấu trúc từng slide theo luật sắt:
   - **1 Slide = 1 Thông điệp cốt lõi.**
   - **Action Title bắt buộc:** Tiêu đề mỗi slide phải là một câu kết luận hoàn chỉnh có chứa insight hoặc con số (VD: *"Phễu Demo-First giúp tối ưu 62% chi phí chuyển đổi"* thay vì *"Phễu chuyển đổi"*).
   - **Quy tắc mật độ:** Tối đa 35 từ/slide, chia thành Bento Grid (2–4 thẻ Card), KPI Callouts (số liệu lớn), Bảng so sánh, hoặc Timeline ngang.

### Pha 2: Phản Biện Khắt Khe & Tự Nâng Cấp (`Red-Team Critic` — `agent-05-quality-gate`)
Trước khi thiết kế, Giám khảo nội bộ phải quét toàn bộ dàn ý slide v1 và tự động sửa sạch 5 lỗi kinh điển:
1. *Lỗi nhiều chữ (Wall of Text)* $\rightarrow$ Rút gọn thành từ khóa đắt giá + thẻ số liệu.
2. *Lỗi tiêu đề chung chung* $\rightarrow$ Viết lại toàn bộ thành Action Titles.
3. *Lỗi thiếu bằng chứng/số liệu* $\rightarrow$ Bổ sung bảng phân bổ ngân sách, KPI định lượng, mốc thời gian cụ thể.
4. *Lỗi bố cục đơn điệu (2 slide liên tiếp giống hệt nhau)* $\rightarrow$ Đổi sang bố cục đa dạng (Slide 1: Hero Cover, Slide 2: 3 KPI Cards, Slide 3: 2-Column Comparison, Slide 4: 4-Step Flow, Slide 5: Data Table/Matrix, Slide 6: Roadmap...).
5. *Lỗi văn mẫu AI (AI Slop)* $\rightarrow$ Xóa sạch các từ sáo rỗng, thay bằng ngôn ngữ điều hành thực chiến.
*(Chỉ khi điểm hội đồng đạt $\ge 9.0/10$ mới chuyển sang Pha 3).*

### Pha 3: Định Hướng Mỹ Thuật & Hệ Thống Token (`Brand Director` — `agent-18-brand-designer`)
Chọn 1 trong 2 phong cách thẩm mỹ cao cấp (hoặc theo yêu cầu):
1. **Area Editorial Luxury (Sáng & Sang trọng):**
   - Nền kem ấm (`#FAF8F5` / `#FFFFFF`), chữ đen sâu (`#111111`), màu nhấn xanh Olive (`#485C11` & `#8E9C78`) và nền thẻ xanh nhạt (`#DFECC6`), bo góc `24px–30px`, kết hợp tiêu đề Serif cổ điển (`Crimson Text` / `Playfair Display`) + nội dung Sans-serif (`DM Sans` / `Inter`) + số liệu `Roboto Mono`.
2. **Precision Dark Tech (Tối & Hiện đại kiểu Linear/Vercel):**
   - Nền đen sâu (`#090A0F`), thẻ bề mặt (`#12151E`), viền mảnh `1px rgba(255,255,255,0.08)`, chữ trắng `#F8FAFC`, điểm nhấn xanh Emerald/Indigo, số liệu Monospace sắc nét.

### Pha 4: Tự Động Xuất File & Kiểm Định Thực Tế (`Slide Engineer` — `agent-08` & `agent-17`)
Thực thi tự động cả 2 định dạng đầu ra (trừ khi người dùng chỉ yêu cầu 1):
1. **Interactive Web Slide Deck (`<slug>_deck.html`):**
   - File HTML độc lập (Single-file HTML/CSS/JS) chuẩn tỷ lệ `16:9`, responsive, hỗ trợ phím mũi tên `←` / `→` / `Space`, phím `F` toàn màn hình, chỉ báo số trang (`1 / N`), hiệu ứng chuyển slide mượt mà.
2. **Native PowerPoint File (`<slug>_deck.pptx`):**
   - Viết và chạy script Python (`python-pptx`) để xuất file `.pptx` chuẩn `16:9` (`13.333 x 7.5 inches`), vẽ các khối Card bo góc, thanh tiêu đề, hộp KPI và bảng biểu có căn chỉnh tọa độ chuẩn xác.
3. **Self-QA & Pyramid of Trust Verification (`hermes-verify-harness`):**
   - Chạy `/Users/buithiphuongthao/.local/bin/hermes-verify-harness <slug>_deck.html <slug>_deck.pptx` để kiểm chứng tất định: file `.html` và `.pptx` tồn tại trên ổ đĩa, dung lượng hợp lệ, không còn biến template `{{...}}`, không có comment cắt cụt (`<!-- ... rest of slides ... -->`), không chứa từ cấm AI Slop.
