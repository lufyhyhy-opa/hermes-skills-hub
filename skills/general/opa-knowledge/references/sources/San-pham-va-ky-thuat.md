**Owner:** Điện  
**Ngày cập nhật:** 31/10/2026  
**Trạng thái:** Bản nháp chờ duyệt  
**Người duyệt:** Điện, Phương (đúng tính năng); luật sư đọc mục 4 và 5. Đầu ra của việc H5 trong `01-Strategy/Ho-so-nang-luc-2026/Ke-hoach-ho-so-nang-luc-OPA.md` (hạn T6 13/11). Không thay file nào.

# Sản phẩm OPA tự xây (trang 7) và Kỹ thuật, an toàn dữ liệu (trang 12)

> **Cách đọc.** File này soạn chữ cho trang 7 và trang 12 của hồ sơ năng lực v1, kèm danh sách ảnh màn hình, kịch bản video 60 giây và sơ đồ dữ liệu. Câu về sản phẩm lấy từ trang công khai đọc sáng 31/10/2026 (giờ Việt Nam) hoặc từ câu Minh đã duyệt ngày 30/10. Ký hiệu: **[P]** Phương xác nhận rồi mới in · **[LS]** luật sư đọc · **?** chưa có nguồn, không in. Tình trạng chỉ có 2 nhãn: **Đang làm** (có nguồn ghi rõ) và **Đang hoàn thiện** (chưa làm, hoặc chưa có bằng chứng). Không ghi giá (Minh chốt 30/10). Không có số người dùng, số kết quả hay lời khen vì chưa có nguồn.

## 1. Kết luận nhanh

1. **Trang 7 đủ chữ cho 4 thẻ, chưa có ảnh.** Tình trạng theo trang công khai: OPA Agent: **đang bán** (gói trả phí kích hoạt qua email, trang ghi chưa nhận thanh toán online) · Xưởng Media: **đang bán**, OPA dùng cho ảnh, video của đội · OPA CRM: **OPA dùng nội bộ** · Creative Intelligence OS: **mời riêng**.
2. **3 câu cần Phương trước khi in trang 7:** OPA Agent đã có shop thật dùng chưa (kho mã ghi mục chạy thử với shop thật chưa xong; nếu chưa thì đổi nhãn thành "Mở đăng ký dùng thử") · OPA CRM có phần bán hàng, công việc và trợ lý AI đang chạy không (câu Minh đã duyệt, nhưng trang công khai chưa có) · màn hình bên trong Creative Intelligence OS.
3. **Trang 12 phần lớn còn "đang hoàn thiện".** Điều đang làm thật nằm chủ yếu ở OPA Agent: nhân viên tiếp quản bất cứ lúc nào; trang nói rõ AI có thể trả lời sai và nội dung hội thoại đi tới máy chủ AI ở nước ngoài; có chính sách bảo mật, điều khoản (cập nhật 13/10/2026) và trang yêu cầu xoá dữ liệu. Xác thực 2 bước, "2 người biết chạy", chế độ soạn nháp, câu "đây là trợ lý AI", hồ sơ đánh giá tác động đều chưa xong.
4. **Phát hiện mới trên chính sách OPA Agent:** nêu 6 nhà cung cấp mô hình AI và một cổng định tuyến do OPA vận hành; còn 2 ô trống "[Tên pháp nhân]" và "[Khu vực đặt máy chủ]"; câu "khi chuyển dữ liệu ra nước ngoài, OPA thực hiện thủ tục theo quy định" chưa có hồ sơ đứng sau (việc 2 kế hoạch 27/10 còn chờ luật sư).
5. **3 rủi ro luật mới thấy, chờ luật sư:** (a) OPA Agent nói chuyện trực tiếp với khách nên có thể thuộc nhóm rủi ro trung bình của Luật AI; khi đó OPA (bên cung cấp) có thể phải tự bảo đảm khách biết đang nói chuyện với AI và báo kết quả phân loại cho Bộ Khoa học và Công nghệ, không chỉ giao cho shop. (b) Ảnh chuyển khoản có thể là dữ liệu nhạy cảm. (c) Tin nhắc giỏ hàng có thể bị coi là tin quảng cáo, cần đồng ý.
6. **Trước khi chụp, quay (hạn T6 13/11):** xong việc S1 (đổi khóa kho `xuongmedia`); có trang Facebook và Pancake POS thử; có không gian OPA CRM mẫu tách khỏi dữ liệu thật. Không mở kỹ năng vượt CAPTCHA, trình duyệt chống phát hiện trong ảnh và video.

## 2. Trang 7: Sản phẩm OPA tự xây

**Tiêu đề:** Sản phẩm OPA tự xây · **Dòng phụ:** Bốn phần mềm OPA tự viết và đang chạy. · **Chân trang:** Ảnh màn hình dùng dữ liệu mẫu.

### 2.1 Bốn thẻ (bản in)

**Thẻ 1 · OPA Agent: trợ lý AI trả lời tin nhắn fanpage**
- **Một câu:** Khi shop bận, OPA Agent trả lời tin nhắn fanpage và lên đơn vào Pancake POS; nhân viên tiếp quản bất cứ lúc nào.
- **Cho ai:** Shop bán qua fanpage, đang dùng Pancake và Pancake POS.
- **3 việc:** Trả lời theo sản phẩm, giá, tồn kho của shop · Lên đơn vào Pancake POS khi khách đồng ý mua · Đối chiếu ảnh chuyển khoản, chưa khớp thì chuyển nhân viên duyệt.
- **Tình trạng:** Đang bán [P]
- **Link:** chat.overpowers.agency · **Ảnh:** A1 (mục 3.3)

**Thẻ 2 · OPA CRM**
- **Một câu (Minh duyệt 30/10, mục 12.1 số 5):** Quản lý khách hàng, bán hàng và công việc ở một chỗ, có trợ lý AI trả lời trên dữ liệu công ty. OPA đang dùng cho chính mình. *Chỗ chật: bỏ cụm "trả lời trên dữ liệu công ty".*
- **Cho ai:** Đội bán hàng và đội marketing của doanh nghiệp vừa và nhỏ.
- **3 việc:** Quản lý khách hàng ở một chỗ · Theo dõi dự án quảng cáo trên Facebook, Google, TikTok, YouTube · Hỏi trợ lý AI trên dữ liệu công ty [P].
- **Tình trạng:** OPA dùng nội bộ
- **Link:** crm.overpowers.agency (trang đăng nhập; chưa đặt mã QR, xem 2.3) · **Ảnh:** C1

**Thẻ 3 · Xưởng Media: xưởng làm ảnh, video bằng AI**
- **Một câu:** Tải ảnh sản phẩm lên, chọn mô hình AI, tải ảnh và video về dùng ngay; làm trên web, thanh toán bằng tiền Việt, không cần thẻ quốc tế.
- **Cho ai:** Người làm nội dung, shop bán online, người làm tiếp thị liên kết và agency cần nhiều ảnh, video.
- **3 việc:** Ảnh sản phẩm nền studio, xóa nền, nâng nét · Video ngắn từ ảnh hoặc từ chữ · Kéo thả quy trình để làm hàng loạt, không cần lập trình.
- **Tình trạng:** Đang bán · OPA dùng cho ảnh, video của đội
- **Link:** xuongmedia.com · **Ảnh:** X1 (ghi nhãn "Ảnh tạo bằng AI")

**Thẻ 4 · Creative Intelligence OS: nơi làm nội dung cho chủ doanh nghiệp**
- **Một câu:** Từ thông tin thật đến nội dung có giá trị: gom nguồn tham khảo, chọn hướng, rồi viết nội dung khớp thương hiệu.
- **Cho ai:** Chủ doanh nghiệp và chuyên gia ở doanh nghiệp vừa và nhỏ Việt Nam.
- **3 việc:** Gom nguồn tham khảo · Giúp ra quyết định nội dung · Làm nội dung khớp thương hiệu và khách hàng.
- **Tình trạng:** Mời riêng (đang mời dùng thử)
- **Link:** creative.overpowers.agency (trang đăng nhập; chưa đặt mã QR) · **Ảnh:** I1, hoặc I2 nếu được xác nhận

### 2.2 Nguồn từng câu (để A2, A7 kiểm)

| Thẻ | Câu hoặc ý | Nguồn (đọc 31/10/2026) | Ghi chú |
|---|---|---|---|
| OPA Agent | Trả lời khách, lên đơn vào Pancake POS | chat.overpowers.agency: "OPA trả lời khách, chốt đơn vào Pancake POS." | |
| | Theo sản phẩm, giá, tồn kho | Trang chủ: "theo sản phẩm, giá, tồn kho của shop"; "OPA đọc sản phẩm, tồn kho và tạo đơn thẳng vào POS." | Giá ở đây là giá hàng của shop, không phải giá OPA |
| | Đối chiếu ảnh chuyển khoản | Trang chủ: "Khớp thì OPA tự ghi nhận đã thanh toán vào đơn Pancake POS, chưa khớp thì chuyển nhân viên duyệt." | |
| | Nhân viên tiếp quản | Trang chủ: "Khi nhân viên trả lời, AI tạm dừng."; điều khoản: "Nhân viên có thể tiếp quản bất cứ lúc nào." | |
| | Cho shop dùng Pancake, Pancake POS | Trang chủ, phần câu hỏi: cần gói Pancake đang chạy, trang đã kết nối và Pancake POS | |
| | Đang bán | /pricing có các gói trả phí; điều khoản: "Hiện OPA chưa nhận thanh toán online", khách gửi email để kích hoạt gói | [P] Kế hoạch 30/10 mục 9.1: kho mã ghi mục "chạy thử với shop thật" chưa xong. Chưa có shop thật dùng thì đổi nhãn "Mở đăng ký dùng thử" |
| | OPA dùng cho chính mình | Chưa: việc 5 kế hoạch 27/10 (bật trên fanpage OPA, T6 06/11) | Thêm dòng này khi việc 5 xong |
| OPA CRM | Câu giới thiệu | Kế hoạch 30/10 mục 12.1 số 5 (Minh duyệt 30/10) | |
| | Quản lý khách hàng | crm.overpowers.agency: "Quản lý khách hàng, dự án OPA Agency" | |
| | Dự án quảng cáo 4 nền tảng | Trang đăng nhập: "Nền tảng quản lý khách hàng, dự án quảng cáo đa nền tảng cho đội ngũ marketing chuyên nghiệp", kèm Facebook, Google, TikTok, YouTube | |
| | Bán hàng, công việc, trợ lý AI | Chưa có trên trang công khai; kho mã có "5 trợ lý AI trả lời câu hỏi trên dữ liệu công ty" (kế hoạch 30/10 mục 9.1 số 3) | [P] |
| | OPA dùng nội bộ | Mục 12.1 số 5; mục 9.1 số 3 (tài liệu triển khai trong kho) | Trang đăng nhập có nút "Đăng ký": [P] có mở cho người ngoài tự đăng ký không |
| | Cho ai | Câu định vị Minh chốt 30/10; trang đăng nhập ghi "đội ngũ marketing" | |
| Xưởng Media | Sản phẩm của OPA | Minh chốt 30/10 (mục A6) | Chân trang xuongmedia.com chỉ ghi "© 2026 Xưởng Media." |
| | Ảnh nền studio, xóa nền, nâng nét | xuongmedia.com: mục bán hàng (ảnh studio, tạo nền, xóa vật thể), mục chỉnh sửa (nâng cấp 4K, xóa nền) | Không in "chỉ trong vài giây", "chỉ với 1 click" |
| | Video từ ảnh hoặc chữ | Trang chủ: "Text → Video / Image → Video" | |
| | Kéo thả quy trình, không cần lập trình | Trang chủ: "Kéo thả pipeline AI, tự động hoá quy trình sản xuất nội dung"; "Không cần lập trình" | |
| | Tiền Việt, không cần thẻ quốc tế | Trang chủ: "thanh toán bằng VND"; "Không cần thẻ quốc tế." | |
| | Cho ai | Trang chủ: 3 nhóm người dùng (người làm affiliate, người làm nội dung, người thích tự động hóa ở agency) và mục bán hàng | |
| | Đang bán | Trang chủ có bảng giá 3 gói và nút đăng ký | Không chép giá |
| | OPA dùng cho ảnh, video của đội | Kế hoạch 27/10 mục 3, bảng sẵn sàng bán | |
| Creative Intelligence OS | Câu chính | creative.overpowers.agency: "Từ thông tin thật đến nội dung có giá trị." | |
| | 3 việc | Trang: "CI·OS giúp bạn tập hợp nguồn tham khảo, đưa ra quyết định và tạo nội dung phù hợp với thương hiệu và khách hàng." | Trang không nói có AI: thẻ không ghi chữ AI |
| | Cho ai | Mô tả trang: "Hệ điều hành sáng tạo nội dung cho founder/expert SME Việt Nam." | |
| | Mời riêng | Trang: "Chỉ dành cho thành viên được mời trong tổ chức."; nhãn "đang mời dùng thử" theo kế hoạch 30/10 mục 9.2 | |
| | OPA dùng nội bộ | Chưa xác nhận: việc 6 kế hoạch 27/10 (lịch nội dung tháng 11–12 trên Creative Intelligence OS, T6 06/11) | Chưa in |

### 2.3 Không in ở trang 7

- Giá, tên gói, xu, hạn mức hội thoại (Minh chốt 30/10). Em đọc /pricing chỉ để biết OPA Agent đang bán.
- Các con số ở đầu trang Xưởng Media (số ứng dụng, số câu lệnh mẫu, số mô hình, số người dùng): mục 12.1 số 8. Trang ghi "59+" mô hình còn kho mã ghi "hơn 20" (mục 9.2): lệch, không in.
- Dải logo các hãng AI và các nhãn tự khen trên trang Xưởng Media: OPA không có giấy đối tác (kế hoạch 30/10 mục 5 số 12).
- Số shop, số hội thoại, số khách, lời khen: chưa có (việc 12, 13 kế hoạch 27/10).
- "Meta đã duyệt ứng dụng ngày 16/06": chỉ có trong 1 tài liệu ở kho riêng tư, chưa rõ năm; trang công khai lại ghi không cần tạo app Facebook.
- Cảnh "khách nhắn lúc nửa đêm vẫn được trả lời" nếu thiếu điều kiện trang nêu: AI đang bật, kết nối ổn định, còn hạn mức.
- PowerPack WMS: để ở trang 10 (mục 12.1 số 7).
- Mã QR: OPA Agent và Xưởng Media trỏ trang sản phẩm; OPA CRM và Creative Intelligence OS chỉ có trang đăng nhập, nên trỏ video 60 giây khi có link (việc 4) hoặc bỏ. Thêm `utm_content=hoso-v1` nếu trang đo được (giống việc H8).

### 2.4 Chỗ lệch trên trang công khai (chuyển A1, Ánh, Phương)

- Tên thương hiệu: chân trang OPA Agent ghi "OverPowers Agency", tiêu đề trang OPA CRM ghi "OPA CRM — OverPowers Agency"; tên đã chốt là "Over Powers Agency" (A5).
- Email: chính sách và trang xoá dữ liệu OPA Agent để email dạng ẩn; công cụ đọc ra privacy@opa.business và hi@opa.business (cần mở trang kiểm lại). Email đã chốt cho hồ sơ là overpowersagency@gmail.com (A4).
- Chính sách bảo mật và điều khoản OPA Agent còn ô trống "[Tên pháp nhân]", "[Khu vực đặt máy chủ]". Tên pháp nhân điền theo kết quả tra của A1.
- Trang đăng nhập OPA CRM vẫn ghi câu cũ (E1), chưa có link chính sách bảo mật, điều khoản.
- Trang chủ Xưởng Media chưa có link chính sách bảo mật, điều khoản, liên hệ, chưa có dòng "Sản phẩm của Over Powers Agency" (A6).
- Trang đăng nhập Creative Intelligence OS ghi "Bằng việc tiếp tục, bạn đồng ý với chính sách bảo mật của Creative Intelligence OS." nhưng chữ "chính sách bảo mật" chưa có link.

## 3. Ảnh màn hình và video 60 giây

### 3.1 Luật khi chụp, quay

1. **Chỉ dữ liệu mẫu** (mục 3.2). Góc ảnh ghi "Dữ liệu mẫu". Không mở trang, CRM hay tài khoản có dữ liệu thật của OPA hoặc của khách.
2. **Không lộ khóa:** mã kết nối Pancake, khóa Pancake POS, khóa gọi AI, mật khẩu, email và số điện thoại thật không được lên hình; kiểm cả thanh địa chỉ, thông báo, lịch sử trình duyệt. Dùng hồ sơ trình duyệt sạch (không tiện ích, không dấu trang).
3. **Không mở** kỹ năng vượt CAPTCHA và trình duyệt chống phát hiện trong `opa-crm`, `opa-kit` (mục 9.4, S4); 9 kho ở mục 9.3; mã nguồn; kho riêng tư (mục 9.5).
4. **Không giá:** không chụp bảng giá, ví xu, trang nâng gói.
5. **Nhãn AI:** ảnh do AI tạo hoặc chỉnh mạnh ghi "Ảnh tạo bằng AI"; video có cảnh hoặc giọng do AI tạo ghi "Video có nội dung do AI tạo" (việc 4 kế hoạch 27/10; Luật AI Điều 11). Không dùng ảnh người thật làm đầu vào cho AI; không đổi mặt, không nhân bản giọng người thật.
6. **Người đứng hình** (anh Huy hoặc Minh, theo việc 4) đã ký phiếu đồng ý dùng tên và ảnh (việc H3). Dùng giọng thật.
7. **Điều kiện trước khi quay:** S1 xong (đổi khóa kho `xuongmedia`, mục 9.2 và 9.4; phiếu việc `Viec-S1-doi-khoa-kho-xuongmedia.md`, hạn T6 06/11); có trang Facebook thử nối Pancake và Pancake POS thử [P]; có không gian OPA CRM mẫu tách khỏi dữ liệu thật [P]; có tài khoản Creative Intelligence OS thử [P].
8. **Lưu và duyệt:** ảnh vào `05-Media/Ho-so-nang-luc-2026/anh-san-pham/`, tên file theo mã ở 3.3 kèm ngày chụp; khung 16:9, tối thiểu 1920×1080. Phương duyệt tính năng đúng, Thành duyệt hình.

### 3.2 Dữ liệu mẫu dùng chung

| Dùng cho | Dữ liệu mẫu | Tránh |
|---|---|---|
| Shop (OPA Agent) | "Tiệm Áo Mẫu" bán áo thun: 3 mẫu (trắng, đen, xanh), size S đến XL, giá và tồn kho mẫu. Lưu ý cho AI: "Khách hỏi đổi trả thì chuyển nhân viên" | Tên, sản phẩm của shop thật |
| Khách của shop | "Khách Mẫu 01" đến "05", ảnh đại diện là khối màu; số điện thoại che dạng 09xx xxx x01; địa chỉ "Số 1 Đường Mẫu" | Ảnh, tên người thật |
| Ảnh chuyển khoản | 2 ảnh tự dựng: "Ngân hàng Mẫu", số tài khoản 0000 0000 0001, chữ "ẢNH MẪU" chạy chéo; 1 ảnh khớp số tiền đơn, 1 ảnh lệch | Logo, giao diện ngân hàng thật |
| Doanh nghiệp (OPA CRM) | "Công ty Mẫu A" đến "J", người liên hệ "Anh Mẫu", "Chị Mẫu"; ngành spa, thời trang, quán cà phê; dự án "Chiến dịch Mẫu tháng 11" trên 4 nền tảng, số liệu mẫu | Danh sách 30 chủ doanh nghiệp của anh Huy, dữ liệu AI Audit, chi tiêu quảng cáo thật |
| Ảnh sản phẩm (Xưởng Media) | 1 đồ vật thật, không có người, chụp bằng điện thoại trên bàn (Cường chụp) | Ảnh chân dung, ảnh có mặt người |
| Nội dung (Creative Intelligence OS) | "Thương hiệu Mẫu"; 3 bài viết công khai về chủ đề "trả lời tin nhắn khách nhanh hơn", ghi rõ nguồn trên màn hình | Tài liệu nội bộ, tên khách |

### 3.3 Ảnh cần chụp (★ là ảnh cho trang 7)

| Mã | Sản phẩm | Màn hình | Dữ liệu mẫu | Dùng ở | Điều kiện |
|---|---|---|---|---|---|
| A1 ★ | OPA Agent | Khung thử AI trong tài khoản: khách hỏi "Áo trắng còn size M không?", AI trả lời theo giá, tồn kho | Tiệm Áo Mẫu | Trang 7, video V1 | Trang Facebook, Pancake POS thử [P] |
| A2 | OPA Agent | Cấu hình AI: chọn giọng (thân thiện, chuyên nghiệp, vui vẻ), cách xưng hô, lưu ý riêng | Lưu ý mẫu | V1, web | |
| A3 | OPA Agent | Đơn vừa tạo trong Pancake POS thử | Khách Mẫu 02 | V1 | Che số điện thoại |
| A4 | OPA Agent | Đối chiếu ảnh chuyển khoản: 1 đơn đã ghi nhận, 1 đơn chờ nhân viên duyệt | 2 ảnh chuyển khoản mẫu | V1, trang 12 | |
| A5 | OPA Agent | Hội thoại sau khi bấm "Tiếp quản" (AI tạm dừng) và công tắc bật, tắt AI | Khách Mẫu 03 | Trang 12 (khối người duyệt), V1 | |
| C1 ★ | OPA CRM | Danh sách khách hàng | Công ty Mẫu A–J | Trang 7, V2 | Không gian mẫu [P] |
| C2 | OPA CRM | Dự án quảng cáo theo 4 nền tảng | Chiến dịch Mẫu tháng 11 | V2 | |
| C3 | OPA CRM | Hỏi trợ lý AI: "Khách nào chưa được liên hệ lại trong 7 ngày?" | Công ty Mẫu | V2 | Chỉ khi Phương xác nhận [P] |
| X1 ★ | Xưởng Media | Ảnh gốc chụp điện thoại đặt cạnh ảnh đã xóa nền, đặt nền studio | Đồ vật mẫu | Trang 7, V3 | S1 xong; nhãn "Ảnh tạo bằng AI" |
| X2 | Xưởng Media | Quy trình kéo thả mẫu "Ảnh sản phẩm": 1 ảnh, nhiều góc, xóa nền, nâng nét | Đồ vật mẫu | V3, web | |
| X3 | Xưởng Media | Tạo video từ ảnh X1 (khung đầu và thanh tiến trình) | Đồ vật mẫu | V3 | Nhãn AI |
| I1 ★ | Creative Intelligence OS | Trang đăng nhập công khai (câu chính và dòng "Chỉ dành cho thành viên được mời") | Không có dữ liệu | Trang 7 | Thay bằng I2 nếu được xác nhận |
| I2 | Creative Intelligence OS | Gom nguồn tham khảo | 3 bài công khai | V4 | Tài khoản thử [P] |
| I3 | Creative Intelligence OS | Chọn hướng nội dung | Thương hiệu Mẫu | V4 | [P] |
| I4 | Creative Intelligence OS | Bản nháp nội dung khớp giọng thương hiệu, có bước người sửa, duyệt | Thương hiệu Mẫu | V4 | [P] |

**Không chụp:** màn hình nhập mã kết nối Pancake, khóa POS (nếu phải quay thì che kín ô) · mục tài chính, nhân sự trong OPA CRM (số nội bộ, dữ liệu nhân viên) · trang đăng nhập OPA CRM hiện tại (câu cũ, E1) đến khi đổi · dải số và dải logo hãng AI ở đầu trang Xưởng Media · người mẫu AI, thay đồ, đổi kiểu tóc, nhân bản video, đổi phong cách theo tác phẩm của người khác · mục Chợ AI (nội dung của người dùng khác) · email thành viên thật trong Creative Intelligence OS.

### 3.4 Kịch bản video 60 giây

Dùng chung với việc 4 kế hoạch 27/10 (Thành phụ trách, Cường dựng, hạn T6 13/11). File này viết 4 video cho 4 thẻ; video thứ 5 (opa.business) không thuộc file này. Mỗi video: 1 người thật nói vào máy (anh Huy hoặc Minh), phần còn lại quay màn hình dữ liệu mẫu; phụ đề tiếng Việt; không số kết quả, không giá; thẻ cuối chỉ có tên và link, không thêm nút (hồ sơ chỉ có 1 nút ở trang 15). Trang OPA Agent đã có 1 video 30 giây kể chuyện shop bỏ sót khách khi bận: Thành xem dùng lại được cảnh nào và kiểm nhãn AI.

**V1 · OPA Agent** · Nhãn "Dữ liệu mẫu" ở đoạn quay màn hình; thêm "Video có nội dung do AI tạo" nếu có cảnh hoặc giọng AI.

| Giây | Hình | Lời | Chữ trên hình |
|---|---|---|---|
| 0–5 | Điện thoại sáng lúc 23:48, tin nhắn "Áo trắng còn size M không shop?" (quay thật, dữ liệu mẫu) | "Gần nửa đêm, khách nhắn hỏi size. Shop đã nghỉ." | 23:48 |
| 5–13 | Người nói vào máy | "OPA Agent là trợ lý AI trả lời tin nhắn fanpage cho shop dùng Pancake. Shop vẫn làm trên Pancake như cũ." | OPA Agent: trợ lý AI trả lời tin nhắn fanpage |
| 13–24 | A1 | "Một: AI trả lời theo sản phẩm, giá, tồn kho mà shop đã nhập." | 1. Trả lời theo sản phẩm, giá, tồn kho |
| 24–34 | A3 | "Hai: khách đồng ý mua thì đơn vào thẳng Pancake POS." | 2. Lên đơn vào Pancake POS |
| 34–44 | A4 | "Ba: khách gửi ảnh chuyển khoản, OPA đối chiếu. Chưa khớp thì chuyển nhân viên duyệt." | 3. Chưa khớp thì người duyệt |
| 44–53 | A5 | "AI có thể trả lời sai. Nhân viên xem lại và bấm Tiếp quản bất cứ lúc nào; shop bật, tắt AI khi cần." | Người tiếp quản bất cứ lúc nào |
| 53–60 | Thẻ cuối | (nhạc) | OPA Agent · chat.overpowers.agency · Over Powers Agency |

Chú thích dưới video (web): "Dữ liệu mẫu. AI chỉ trả lời khi đang bật, kết nối ổn định và còn hạn mức. Để trả lời, OPA gửi nội dung hội thoại tới nhà cung cấp mô hình AI có máy chủ ở nước ngoài." (theo trang OPA Agent) [LS]

**V2 · OPA CRM** · Nhãn "Dữ liệu mẫu" ở đoạn quay màn hình.

| Giây | Hình | Lời | Chữ trên hình |
|---|---|---|---|
| 0–6 | Bàn làm việc, sổ tay, điện thoại nhiều tin nhắn (quay thật, không lộ tin thật) | "Khách hỏi từ tuần trước. Đã ai gọi lại chưa?" | |
| 6–15 | Người nói vào máy | "OPA CRM: quản lý khách hàng, bán hàng và công việc ở một chỗ. OPA đang dùng cho chính mình." | OPA CRM |
| 15–27 | C1 | "Một: khách hàng nằm ở một chỗ, không rải trong sổ tay và tin nhắn riêng." | 1. Khách hàng ở một chỗ |
| 27–39 | C2 | "Hai: dự án quảng cáo trên Facebook, Google, TikTok, YouTube theo dõi chung." | 2. Dự án quảng cáo 4 nền tảng |
| 39–51 | C3 [P] | "Ba: hỏi trợ lý AI ngay trên dữ liệu công ty, ví dụ khách nào chưa được liên hệ lại." | 3. Hỏi trợ lý AI trên dữ liệu công ty |
| 51–60 | Thẻ cuối | (nhạc) | OPA CRM · OPA đang dùng cho chính mình |

Nếu C3 chưa được xác nhận: bỏ đoạn 39–51, kéo dài 2 đoạn trước; video còn khoảng 50 giây.

**V3 · Xưởng Media** · Nhãn "Video có nội dung do AI tạo" suốt video.

| Giây | Hình | Lời | Chữ trên hình |
|---|---|---|---|
| 0–5 | Tay đặt đồ vật lên bàn, chụp bằng điện thoại (quay thật) | "Một tấm ảnh sản phẩm chụp bằng điện thoại." | |
| 5–12 | Người nói vào máy | "Xưởng Media là xưởng làm ảnh và video bằng AI của OPA, chạy ngay trên web." | Xưởng Media |
| 12–25 | X1 | "Một: xóa nền, đặt nền kiểu studio, nâng nét ảnh." | 1. Ảnh sản phẩm · Ảnh tạo bằng AI |
| 25–37 | X3 | "Hai: từ ảnh đó làm một video ngắn." | 2. Video từ ảnh · Video tạo bằng AI |
| 37–50 | X2 | "Ba: kéo thả thành quy trình, chạy cho nhiều ảnh một lượt, không cần lập trình." | 3. Quy trình kéo thả, làm hàng loạt |
| 50–60 | Thẻ cuối | "Thanh toán bằng tiền Việt, không cần thẻ quốc tế." | Xưởng Media · xuongmedia.com · Sản phẩm của Over Powers Agency |

**V4 · Creative Intelligence OS** · Chỉ quay khi I2–I4 được xác nhận [P]. Nhãn "Dữ liệu mẫu".

| Giây | Hình | Lời | Chữ trên hình |
|---|---|---|---|
| 0–6 | Người nói vào máy | "Chủ doanh nghiệp hiểu nghề, nhưng ngồi viết bài thì bí." | |
| 6–15 | I1 | "Creative Intelligence OS là nơi làm nội dung OPA đang mời dùng thử: từ thông tin thật đến nội dung có giá trị." | Đang mời dùng thử |
| 15–28 | I2 | "Một: gom nguồn tham khảo về một chỗ." | 1. Gom nguồn tham khảo |
| 28–40 | I3 | "Hai: chọn hướng nội dung từ những gì đã gom." | 2. Ra quyết định nội dung |
| 40–52 | I4 | "Ba: viết nội dung khớp thương hiệu và khách hàng. Người đọc lại, sửa và duyệt rồi mới đăng." | 3. Khớp thương hiệu · Người duyệt trước khi đăng |
| 52–60 | Thẻ cuối | (nhạc) | Creative Intelligence OS · creative.overpowers.agency · Mời riêng |

## 4. Trang 12: Kỹ thuật và an toàn dữ liệu

> **CHỜ LUẬT SƯ ĐỌC.** Cả mục 4 và mục 5 không in, không đăng web khi luật sư chưa đọc (việc 2 kế hoạch 27/10, hạn T6 20/11). Bản thiết kế giữ nhãn nhỏ "Bản nháp, chờ luật sư đọc" ở góc trang cho tới khi luật sư duyệt.

### 4.1 Bản in (khoảng 150 chữ, A2 rút còn 60–80 chữ)

**Kỹ thuật và an toàn dữ liệu**
Với OPA Agent, dữ liệu của shop thuộc về shop (điều khoản dịch vụ) [LS]. Trang này ghi điều OPA đang làm và điều đang hoàn thiện.

**Cách OPA làm phần mềm:** OPA tự viết 4 sản phẩm đang chạy. OPA Agent có 4.259 phép thử tự động, đều đạt (đếm 30/10/2026) [P]; một mô hình AI kiểm câu trả lời trước khi gửi [P]; mã kết nối được mã hoá trước khi lưu, mỗi shop chỉ thấy dữ liệu của mình [P].

| 5 luật an toàn | Đang làm | Đang hoàn thiện |
|---|---|---|
| 1. AI soạn, người duyệt | Với OPA Agent, nhân viên tiếp quản bất cứ lúc nào | 2 tuần đầu AI chỉ soạn nháp khi OPA dựng cho doanh nghiệp |
| 2. Tài khoản đứng tên khách | Shop tự kết nối trang; ngắt kết nối là OPA xoá mã kết nối | Áp cho gói dựng doanh nghiệp [P] |
| 3. Xác thực 2 bước, phần mềm quản lý mật khẩu | | Cho mọi tài khoản quản trị |
| 4. Hệ thống nào cũng có 2 người biết chạy | | Sổ tài sản ghi 2 người cho mỗi sản phẩm |
| 5. Không dán dữ liệu khách vào công cụ AI cá nhân | Quy tắc chung của đội; ảnh trong hồ sơ chỉ dùng dữ liệu mẫu [P] | |

**Luật AI 134/2025 và Luật Bảo vệ dữ liệu cá nhân 91/2025** [LS]
- Đang làm: nói trước với shop rằng AI có thể trả lời sai và nội dung hội thoại được gửi tới nhà cung cấp mô hình AI có máy chủ ở nước ngoài; có chính sách bảo mật và trang yêu cầu xoá dữ liệu cho OPA Agent.
- Đang hoàn thiện: câu "đây là trợ lý AI" bật sẵn; nhãn nội dung do AI tạo trên video; hồ sơ đánh giá tác động khi dữ liệu ra nước ngoài; chính sách bảo mật cho OPA CRM, Xưởng Media.

### 4.2 Năm luật an toàn: chi tiết và nguồn

| # | Luật | Đang làm (nguồn) | Đang hoàn thiện (việc, hạn) | Cần |
|---|---|---|---|---|
| 1 | AI soạn, người duyệt | OPA Agent: "Khi nhân viên trả lời, AI tạm dừng"; bấm Tiếp quản để tắt AI ở hội thoại đó; ảnh chuyển khoản chưa khớp thì chuyển nhân viên duyệt; shop bật, tắt AI bất cứ lúc nào; trang ghi AI có thể trả lời sai (trang chủ, điều khoản). Hồ sơ này do agent soạn, người duyệt (kế hoạch 30/10 mục 11) | Chế độ chỉ soạn nháp, người duyệt rồi mới gửi, cho 2 tuần đầu khi OPA dựng cho doanh nghiệp; nút tắt khẩn cấp (việc 2 kế hoạch 27/10, T6 13/11). Hôm nay OPA Agent tự gửi khi shop bật AI | [P] ngày xong |
| 2 | Tài khoản đứng tên khách | OPA Agent: shop kết nối trang của mình bằng mã do shop cấp; điều khoản ghi "Dữ liệu của shop thuộc về shop"; khi ngắt kết nối "OPA xoá ngay page access token và API key đã lưu" | Gói dựng cho doanh nghiệp: trang Pancake, mã kết nối, OPA CRM đứng tên khách, OPA chỉ có quyền được cấp (kế hoạch 27/10 mục 10). Áp từ khách doanh nghiệp đầu tiên | [P] đã áp cho khách nào chưa |
| 3 | Xác thực 2 bước, phần mềm quản lý mật khẩu | OPA Agent (chính sách bảo mật): mã kết nối và khóa Pancake POS "được mã hoá AES-256-GCM trước khi lưu"; mật khẩu chỉ lưu dạng băm (PBKDF2-SHA256); kết nối HTTPS; giới hạn tần suất ở thao tác nhạy cảm | Xác thực 2 bước và phần mềm quản lý mật khẩu cho mọi tài khoản quản trị máy chủ, khóa API của nhà cung cấp AI, tài khoản quảng cáo (việc 15, T6 18/12). Đổi khóa đang nằm trong file mẫu ở kho mã (S1–S3 mục 9.4, T6 06/11) | [P] cột 2 chạy đúng như chính sách ghi |
| 4 | Hệ thống nào cũng có 2 người biết chạy | Chưa có bằng chứng | Sổ tài sản có tên 2 người cho mỗi sản phẩm; bảng người giữ đang là đề xuất (việc 15, T6 18/12) | |
| 5 | Không dán dữ liệu khách vào công cụ AI cá nhân | Quy tắc ghi trong luật chung của đội và agent (lệnh giao việc 30/10, luật số 4); ảnh trong hồ sơ chỉ dùng dữ liệu mẫu | Dữ liệu AI Audit nhập vào OPA CRM, không qua công cụ cá nhân (việc 9, bộ mẫu T6 06/11). Xác nhận khóa gọi AI của sản phẩm là tài khoản doanh nghiệp, kể cả cổng 9Router | [P] |

### 4.3 Luật Trí tuệ nhân tạo 134/2025/QH15

Quốc hội thông qua 10/12/2025, hiệu lực 01/03/2026. Nghị định 142/2026/NĐ-CP hướng dẫn (ban hành 30/4/2026, hiệu lực 01/5/2026, theo bài của Luật Việt An). Đọc hiểu của em [LS]: với OPA Agent, OPA là bên cung cấp hệ thống AI, shop là bên triển khai.

| Điều | Luật yêu cầu (tóm tắt) | OPA đang làm | Đang hoàn thiện | Cần |
|---|---|---|---|---|
| Điều 9, Điều 10; Nghị định 142/2026 | Hệ thống AI chia 3 mức rủi ro: cao, trung bình, thấp. Mức trung bình gồm hệ thống có thể làm người dùng nhầm vì không biết mình đang tương tác với AI. Với mức trung bình và cao, bên cung cấp báo kết quả phân loại cho Bộ Khoa học và Công nghệ qua cổng một cửa trước khi đưa vào dùng (Điều 10 khoản 3; Nghị định 142/2026 Điều 12) | Chưa thấy trong tài liệu OPA | Phân loại 4 sản phẩm; nếu OPA Agent ở mức trung bình thì làm thông báo | [LS] |
| Điều 11 khoản 1; Điều 15 khoản 1 | Bên cung cấp bảo đảm hệ thống AI tương tác trực tiếp với con người cho người dùng nhận biết đang tương tác với AI; hệ thống mức trung bình phải minh bạch theo Điều 11 | Chính sách và điều khoản OPA Agent giao shop thông báo cho khách "khi pháp luật yêu cầu" | Câu "đây là trợ lý AI" bật sẵn khi OPA Agent trả lời (việc 2, T6 13/11) | [LS] OPA có phải tự làm không |
| Điều 11 khoản 2 | Bên cung cấp bảo đảm âm thanh, hình ảnh, video do AI tạo được đánh dấu ở định dạng máy đọc | Trang Xưởng Media chưa nói | Dấu máy đọc cho ảnh, video Xưởng Media tạo ra | [P] [LS] |
| Điều 11 khoản 3, 4; Nghị định 142/2026 Điều 18 khoản 2 | Bên triển khai thông báo rõ khi đưa ra công chúng nội dung AI dễ gây nhầm về tính xác thực; nội dung mô phỏng ngoại hình, giọng nói người thật hoặc tái hiện sự kiện thật phải có nhãn dễ nhận biết | Luật viết hồ sơ: ảnh do AI tạo hoặc chỉnh mạnh phải ghi nhãn, không dùng AI đổi mặt người thật (lệnh giao việc 30/10) | Nhãn "có nội dung do AI tạo" trên 5 video trình diễn (việc 4, T6 13/11); nhắc người dùng Xưởng Media ghi nhãn khi làm người mẫu AI | [LS] |
| Quy định chuyển tiếp | Theo tóm tắt đọc được: hệ thống đã chạy trước 01/03/2026 có 12 tháng để làm theo (18 tháng với y tế, giáo dục, tài chính). Chưa thấy số điều | | Xem sản phẩm nào đã chạy trước 01/03/2026 | [LS] số điều, cách áp |

### 4.4 Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15

Quốc hội thông qua 26/6/2025, hiệu lực 01/01/2026. Nghị định 356/2025/NĐ-CP hướng dẫn (ban hành 31/12/2025, hiệu lực 01/01/2026). Vai trò theo chính sách OPA Agent: với dữ liệu hội thoại "shop là bên kiểm soát dữ liệu", "OPA xử lý dữ liệu đó theo chỉ thị của shop"; với tài khoản đăng ký của shop, OPA là bên kiểm soát.

| Điều | Luật yêu cầu (tóm tắt) | OPA đang làm | Đang hoàn thiện | Cần |
|---|---|---|---|---|
| Điều 4 khoản 1; Điều 9 | Chủ thể được biết về việc xử lý dữ liệu của mình; đồng ý phải tự nguyện và biết rõ; im lặng không phải là đồng ý | OPA Agent có chính sách bảo mật công khai (13/10/2026): dữ liệu thu, mục đích, bên nhận, thời gian lưu, quyền của chủ thể | Điền ô trống "[Tên pháp nhân]", "[Khu vực đặt máy chủ]"; chính sách cho OPA CRM, Xưởng Media (trang chưa có link) và Creative Intelligence OS (có nhắc, chưa có link); xin liên hệ và đồng ý khi OPA Agent trả lời fanpage OPA (việc 5); văn bản đồng ý của khách AI Audit (việc 9) | [P] [LS] |
| Điều 14 | Xoá, huỷ dữ liệu khi chủ thể yêu cầu hoặc hết mục đích | Trang yêu cầu xoá dữ liệu: xác nhận trong 2 ngày làm việc, xoá xong trong 20 ngày sau khi xác minh; ngắt kết nối thì xoá ngay mã kết nối; xoá tài khoản thì xoá hoặc ẩn danh trong 20 ngày, trừ dữ liệu luật bắt giữ | Người đọc hộp thư yêu cầu mỗi ngày | [P] |
| Điều 20 | Dùng nền tảng ở ngoài Việt Nam để xử lý dữ liệu thu ở Việt Nam là chuyển dữ liệu xuyên biên giới; phải lập hồ sơ đánh giá tác động chuyển dữ liệu xuyên biên giới | Trang chủ và chính sách OPA Agent nói rõ nội dung hội thoại được gửi tới nhà cung cấp mô hình AI, một số có máy chủ ở nước ngoài, và nêu tên các nhà cung cấp | Hồ sơ đánh giá tác động chuyển dữ liệu ra nước ngoài cho OPA Agent, và cho OPA CRM, Xưởng Media nếu dùng mô hình ở nước ngoài (việc 2, luật sư T6 20/11) | [LS] |
| Điều 21, Điều 22 | Bên kiểm soát lập hồ sơ đánh giá tác động xử lý dữ liệu, gửi 1 bản chính cho cơ quan chuyên trách trong 60 ngày từ khi xử lý; cập nhật khi thay đổi | Chưa thấy | Lập hồ sơ (việc 2) | [LS] OPA hay shop lập |
| Điều 23 | Báo cơ quan chuyên trách không quá 72 giờ từ khi phát hiện sự cố, trong các trường hợp luật nêu | Chính sách: OPA thông báo cho shop bị ảnh hưởng và cơ quan có thẩm quyền theo thời hạn luật định | Quy trình xử lý sự cố: ai làm, trong bao lâu | [P] [LS] |
| Điều 28 | Gửi tin quảng cáo cần khách đồng ý và có cách từ chối | | Xem tin nhắc giỏ hàng (sau 1, 6, 20 giờ) có là tin quảng cáo không | [LS] |
| Điều 30 | Xử lý dữ liệu bằng AI, điện toán đám mây: đúng mục đích, giới hạn trong phạm vi cần thiết, có bảo mật và kiểm soát truy cập | Mỗi shop chỉ thấy dữ liệu của mình; mã kết nối được mã hoá; "OPA không bán dữ liệu cá nhân và không dùng nội dung tin nhắn của shop để quảng cáo" | Ghi rõ nhà cung cấp AI có dùng dữ liệu để huấn luyện mô hình không (chính sách chưa nói) | [P] |
| Điều 33, Điều 38 | Có người hoặc bộ phận bảo vệ dữ liệu, hoặc thuê dịch vụ; doanh nghiệp nhỏ, khởi nghiệp được chọn làm hay chưa trong 5 năm, trừ doanh nghiệp kinh doanh dịch vụ xử lý dữ liệu cá nhân, xử lý dữ liệu nhạy cảm hoặc quy mô lớn | Chưa thấy | Chỉ định người phụ trách bảo vệ dữ liệu | [LS] OPA có được chọn hoãn không |
| Nghị định 356/2025 (danh mục dữ liệu nhạy cảm) | Danh mục có "thông tin tài chính, tín dụng và các thông tin về hoạt động, lịch sử giao dịch tài chính" | OPA Agent đọc ảnh chuyển khoản bằng mô hình AI để đối chiếu | Xem có cần đồng ý riêng hay biện pháp bảo vệ thêm | [LS] |
| Điều 8 | Mức phạt theo bản tin luật sư: tới 5% doanh thu năm trước với vi phạm về chuyển dữ liệu xuyên biên giới; tối đa 3 tỷ đồng với vi phạm khác | | | Chỉ để biết mức rủi ro, không in |

### 4.5 Câu không viết (đến khi có giấy hoặc luật sư duyệt)

- "Tuân thủ đầy đủ" Luật AI hay Luật 91/2025; "đã đánh giá tác động", "đã nộp hồ sơ".
- "Dữ liệu lưu tại Việt Nam", "dữ liệu không ra nước ngoài": trang OPA Agent ghi điều ngược lại, nơi đặt máy chủ chính chưa điền.
- "Nhà cung cấp AI không dùng dữ liệu của bạn để huấn luyện": chính sách chưa nói.
- "Đạt chuẩn", "được chứng nhận", "đối tác chính thức" của Meta, Pancake hay hãng AI: chưa có giấy; chân trang OPA Agent tự ghi là sản phẩm độc lập, kết nối qua API công khai của Pancake.
- Mọi lời hứa tuyệt đối về an toàn, hay về việc AI không sai: trang OPA Agent ghi AI có thể trả lời sai.
- "Khách luôn được báo đang nói chuyện với AI": câu báo AI chưa bật sẵn.

## 5. Sơ đồ "dữ liệu khách đi đâu" khi dùng OPA Agent

> **CHỜ LUẬT SƯ ĐỌC.** Mọi câu trong sơ đồ lấy từ trang chủ, chính sách bảo mật, điều khoản (2 trang này ghi cập nhật 13/10/2026) và trang yêu cầu xoá dữ liệu của OPA Agent, đọc 31/10/2026.

**Bố cục cho người thiết kế:** 4 khối xếp ngang theo thứ tự 1 → 2 → 3 → 4, một mũi tên quay về khối 1, một dải ghi chú dưới chân. Màu: khối của shop xám nhạt; khối của OPA xanh #0068FF; khối máy chủ AI viền cam (có máy chủ ở nước ngoài); phần đang hoàn thiện vẽ nét đứt. Mỗi khối tối đa khoảng 12 chữ, chi tiết đưa xuống chú thích nhỏ. Không dùng logo hãng nào.

```text
Khách nhắn tin vào fanpage của shop
          │
          ▼
[1 Trang Pancake của shop] ──①──▶ [2 OPA Agent] ──②──▶ [3 Máy chủ AI] ──③──▶ [4 Người duyệt]
          ▲                                                                        │
          └──────────────────────── ④ câu trả lời, đơn ◀───────────────────────────┘
```

| Phần | Chữ trên hình | Chú thích nhỏ | Nguồn |
|---|---|---|---|
| Khối 1 (xám) | Trang Pancake của shop | Khách nhắn fanpage. Trang, Pancake, Pancake POS đứng tên shop | Trang chủ OPA Agent; điều khoản: "Dữ liệu của shop thuộc về shop" |
| Mũi tên ① | Tin nhắn và đơn hàng | Tin nhắn, tên hiển thị, ảnh đại diện, số điện thoại và địa chỉ khách tự gửi, ảnh chuyển khoản; sản phẩm, giá, tồn kho, đơn từ Pancake POS. Đi qua mã kết nối do shop cấp | Chính sách bảo mật, mục "Dữ liệu OPA thu thập" |
| Khối 2 (xanh) | OPA Agent | Lưu hội thoại, khách, đơn để shop xem. Mỗi shop chỉ thấy dữ liệu của mình. Mã kết nối được mã hoá trước khi lưu. Nơi đặt máy chủ: ? | Chính sách bảo mật, mục "Bảo mật dữ liệu"; ô "[Khu vực đặt máy chủ]" chưa điền [P] |
| Mũi tên ② (cam) | Nội dung hội thoại | Nội dung hội thoại và thông tin sản phẩm cần để trả lời; ảnh chuyển khoản để đọc | Trang chủ: "Để trả lời, OPA gửi nội dung hội thoại tới nhà cung cấp mô hình AI có máy chủ ở nước ngoài." |
| Khối 3 (viền cam) | Máy chủ AI của nhà cung cấp mô hình | Một số ở nước ngoài. Shop chọn mô hình, hoặc dùng mô hình mặc định của OPA | Chính sách bảo mật, mục "Xử lý bằng AI" |
| Mũi tên ③ | Câu trả lời | Một mô hình AI do OPA chọn kiểm câu trả lời trước khi gửi | Chính sách bảo mật [P] |
| Khối 4 (xám, nửa dưới nét đứt) | Người duyệt: nhân viên shop | Đang làm: xem lại, bấm Tiếp quản là AI dừng ở hội thoại đó; duyệt ảnh chuyển khoản chưa khớp; bật, tắt AI bất cứ lúc nào. Đang hoàn thiện (nét đứt): duyệt từng câu trước khi gửi | Trang chủ, điều khoản; việc 2 kế hoạch 27/10 |
| Mũi tên ④ | Câu trả lời, đơn | Câu trả lời gửi khách trên fanpage; đơn ghi vào Pancake POS | Trang chủ |
| Dòng dưới mũi tên ③ và ④ | Hôm nay: khi shop bật AI, câu trả lời được gửi ngay; người duyệt theo dõi và tiếp quản | | Trang chủ, mục câu hỏi |
| Dải ghi chú 1 | Không đi đâu khác | "OPA không bán dữ liệu cá nhân và không dùng nội dung tin nhắn của shop để quảng cáo." | Chính sách bảo mật |
| Dải ghi chú 2 | Xoá | Ngắt kết nối: OPA xoá ngay mã kết nối. Yêu cầu xoá: xác nhận trong 2 ngày làm việc, xoá xong trong 20 ngày sau khi xác minh. Dữ liệu trên Pancake do shop quản lý | Điều khoản; trang yêu cầu xoá dữ liệu |

**Chưa ghi lên sơ đồ, chờ trả lời:** nơi đặt máy chủ chính của OPA Agent [P] · nước đặt máy chủ của từng nhà cung cấp mô hình [P] · nhà cung cấp có dùng dữ liệu để huấn luyện không [P] · in tên các nhà cung cấp lên trang hay chỉ dẫn link chính sách [LS]. Theo chính sách (13/10/2026), nhà cung cấp mô hình "hiện gồm Anthropic, OpenAI, OpenRouter, Google Gemini, Ollama Cloud và Zhipu AI", trong đó Zhipu AI dùng "mô hình GLM, qua cổng định tuyến 9Router do OPA vận hành"; hạ tầng gồm Supabase (cơ sở dữ liệu), Upstash (hàng đợi xử lý), Sentry (theo dõi lỗi).

## 6. Câu cần Phương xác nhận

1. Nhãn "Đang bán" của OPA Agent: đã có shop thật dùng chưa? Chưa thì đổi thành "Mở đăng ký dùng thử" (mục 2.1, 2.2).
2. OPA CRM: phần bán hàng, công việc và trợ lý AI trả lời trên dữ liệu công ty đang chạy (câu Minh đã duyệt, nhưng trang công khai chưa có); nút "Đăng ký" ở trang đăng nhập có mở cho người ngoài không (thẻ 2, C3, V2).
3. Creative Intelligence OS: màn hình gom nguồn, chọn hướng, bản nháp có trong bản đang mời; ai cấp tài khoản thử (I2–I4, V4).
4. Tính năng an toàn ghi trên chính sách OPA Agent chạy đúng: mã hoá mã kết nối, băm mật khẩu, mỗi shop chỉ thấy dữ liệu của mình, mô hình AI kiểm câu trả lời trước khi gửi (mục 4.1, 4.2, 5).
5. Số 4.259 phép thử tự động của OPA Agent: đếm lại ngày in (mục 4.1).
6. Nơi đặt máy chủ chính và vùng của Supabase, Upstash, Sentry; nhà cung cấp mô hình nào đang bật thật, máy chủ ở nước nào; nhà cung cấp có dùng dữ liệu để huấn luyện không (mục 5).
7. Cổng định tuyến 9Router do OPA vận hành: chạy ở đâu, có lưu nội dung hội thoại không, có gọi mô hình bằng khóa trả phí của tài khoản doanh nghiệp không (không qua tài khoản đăng nhập cá nhân kiểu kho `opa-api` ở mục 9.3) (luật 5, mục 5).
8. Hộp thư nhận yêu cầu xoá dữ liệu: địa chỉ thật, ai đọc mỗi ngày, quy trình xoá đã chạy thử chưa (mục 2.4, 4.4).
9. Ngày xong chế độ soạn nháp, câu "đây là trợ lý AI" bật sẵn, nút tắt khẩn cấp (việc 2) (mục 4.2, 4.3).
10. "Tài khoản đứng tên khách" đã áp cho khách doanh nghiệp nào chưa; chưa thì ghi "áp từ khách đầu tiên" (mục 4.2).
11. Có trang Facebook thử, Pancake POS thử, không gian OPA CRM mẫu, tài khoản Creative Intelligence OS thử để chụp, quay trước T6 13/11 (mục 3.1).
12. Xưởng Media có gắn dấu máy đọc cho ảnh, video tạo ra không; OPA CRM và Xưởng Media gửi dữ liệu tới nhà cung cấp AI nào (mục 4.3, 4.4).

## 7. Câu cần luật sư

1. Toàn bộ mục 4.1 (bản in trang 12) và mục 5 (sơ đồ), đặc biệt câu "Với OPA Agent, dữ liệu của shop thuộc về shop" và chú thích dưới video V1.
2. Luật AI Điều 9, 10, 11 khoản 1, Điều 15 và Nghị định 142/2026: OPA Agent có thuộc mức rủi ro trung bình không; nếu có, OPA có phải tự bảo đảm khách biết đang nói chuyện với AI và báo kết quả phân loại cho Bộ Khoa học và Công nghệ trước khi dùng. Chính sách hiện giao shop thông báo "khi pháp luật yêu cầu": có đủ không.
3. Luật AI Điều 11 khoản 2, 4 và Nghị định 142/2026 Điều 18: Xưởng Media có phải đánh dấu máy đọc ảnh, video tạo ra; ai chịu nhãn khi người dùng làm người mẫu AI.
4. Quy định chuyển tiếp của Luật AI (12 tháng, 18 tháng): số điều, sản phẩm nào của OPA được áp.
5. Luật 91/2025 Điều 20: hồ sơ đánh giá tác động chuyển dữ liệu ra nước ngoài cho OPA Agent (và OPA CRM, Xưởng Media nếu dùng mô hình ở nước ngoài): OPA hay shop lập, thời hạn; câu "OPA thực hiện thủ tục theo quy định" trên chính sách hiện có đúng không. Mức phạt ở Điều 8 cho thấy đây là chỗ rủi ro cao.
6. Luật 91/2025 Điều 21, 22, 33, 38: OPA phải lập hồ sơ đánh giá tác động xử lý và chỉ định người bảo vệ dữ liệu ngay, hay được chọn hoãn 5 năm, khi OPA làm dịch vụ xử lý dữ liệu cho shop.
7. Nghị định 356/2025: ảnh chuyển khoản có là dữ liệu nhạy cảm không; cần đồng ý riêng hay biện pháp gì thêm.
8. Luật 91/2025 Điều 28: tin nhắc giỏ hàng sau 1, 6, 20 giờ có là tin quảng cáo cần đồng ý và cách từ chối không.
9. Luật 91/2025 Điều 23 và hợp đồng: quy trình báo sự cố 72 giờ; mẫu hợp đồng xử lý dữ liệu giữa OPA và khách doanh nghiệp (AI Audit nhập 90 ngày dữ liệu khách vào OPA CRM, bật OPA Agent soạn nháp trên fanpage của khách).
10. Có in tên các nhà cung cấp mô hình AI trên trang 12 không, hay chỉ dẫn link chính sách bảo mật.

## 8. Nguồn

**Tài liệu OPA:** `01-Strategy/Ke-hoach-phat-trien-5-san-pham-theo-pheu-G0-G5.md` (mục 3, 4, 4.2, 7, 9, 10) · `01-Strategy/Ho-so-nang-luc-2026/Ke-hoach-ho-so-nang-luc-OPA.md` (mục 4, 5, 6, 7, 9, 12.1) · `01-Strategy/Ho-so-nang-luc-2026/Lenh-giao-viec-7-agent.md` (luật chung, lệnh A5).

**Trang công khai OPA, đọc sáng 31/10/2026 (giờ Việt Nam):** [chat.overpowers.agency](https://chat.overpowers.agency/) · [bảng giá](https://chat.overpowers.agency/pricing) (chỉ để biết đang bán, không chép giá) · [chính sách bảo mật](https://chat.overpowers.agency/privacy) và [điều khoản](https://chat.overpowers.agency/terms) (cùng ghi cập nhật 13/10/2026) · [yêu cầu xoá dữ liệu](https://chat.overpowers.agency/data-deletion) · [crm.overpowers.agency](https://crm.overpowers.agency/) · [xuongmedia.com](https://xuongmedia.com/) · [creative.overpowers.agency](https://creative.overpowers.agency/). Máy chủ của phiên này bị cổng mạng chặn tải thẳng các trang trên (lỗi 403), nên em đọc qua công cụ đọc web. Công cụ trả tóm tắt và câu trích ngắn: trước khi in, người duyệt mở lại trang để so các câu trong ngoặc kép. Em không đăng nhập, không đăng ký, không điền form.

**Luật (đọc hiểu, cần luật sư xác nhận):**
- [GV Lawyers, bản tin Luật Bảo vệ dữ liệu cá nhân 2025](https://gvlawyers.com.vn/wp-content/uploads/2025/09/VN_Legal-alert-_Law-on-PDP-2025.pdf): ngày thông qua, hiệu lực; Điều 8, 20, 30, 33, 38.
- [EY Việt Nam, bản tin 07/2025](https://www.ey.com/content/dam/ey-unified-site/ey-com/vi-vn/technical/tax/documents/legal-alert-july-2025-personal-data-protection-law-vn.pdf): mức phạt, 72 giờ, dùng máy chủ nước ngoài vẫn là chuyển dữ liệu xuyên biên giới (không ghi số điều).
- [Kế toán An Pha, bản chép Luật 91/2025](https://ketoananpha.vn/luat-bao-ve-du-lieu-ca-nhan-nam-2025): mục lục 39 điều; Điều 2, 9, 20, 21, 23, 30.
- [Hệ thống pháp luật, Luật Bảo vệ dữ liệu cá nhân 2025](https://hethongphapluat.com/luat-bao-ve-du-lieu-ca-nhan-2025.html) (đọc được tới Điều 28): Điều 9, 20, 21, 23; phần doanh nghiệp nhỏ 5 năm.
- [LuatVietnam, toàn văn Luật 91/2025](https://luatvietnam.vn/dan-su/tai-toan-van-luat-bao-ve-du-lieu-ca-nhan-2025-pdf-word-568-103646-article.html): hiệu lực 01/01/2026; Điều 21, 22, 33.
- [Cổng phổ biến pháp luật Cần Thơ, 12/03/2026](https://pbgdpl.cantho.gov.vn/quy-dinh-ve-danh-muc-du-lieu-ca-nhan-co-ban-va-danh-muc-du-lieu-ca-nhan-nhay-cam): danh mục dữ liệu nhạy cảm ở Nghị định 356/2025/NĐ-CP.
- [Hệ thống pháp luật, Luật Trí tuệ nhân tạo 134/2025](https://hethongphapluat.com/law-no-134-2025-qh15-dated-december-10-2025-on-artificial-intelligence.html) (đọc được Điều 1–28): Điều 9, 10, 11, 15; ngày thông qua, hiệu lực; tóm tắt quy định chuyển tiếp.
- [Báo Đại biểu Nhân dân, 09/04/2026](https://daibieunhandan.vn/trach-nhiem-minh-bach-trong-quan-ly-he-thong-tri-tue-nhan-tao-duoc-quy-dinh-nhu-the-nao-10412799.html): Điều 11.
- [Apolat Legal](https://apolatlegal.com/vi/laws/luat-tri-tue-nhan-tao-2025-so-134-2025-qh15/): ngày thông qua, hiệu lực, 3 mức rủi ro.
- [Luật Việt An, Nghị định 142/2026/NĐ-CP](https://luatvietan.vn/nghi-dinh-142-2026-nd-cp-huong-dan-luat-tri-tue-nhan-tao.html): ngày ban hành, hiệu lực; tiêu chí rủi ro trung bình; Điều 12, Điều 18 khoản 2.

**Không mở được:** tải thẳng 5 trang sản phẩm từ máy chủ của phiên (cổng mạng chặn, lỗi 403; đã đọc lại qua công cụ đọc web) · thuvienphapluat.vn (Luật 91/2025 bản tiếng Anh, Luật Trí tuệ nhân tạo): trang báo lỗi · luatminhkhue.vn (bài về nhãn nội dung AI): trang báo lỗi · toàn văn chính thức của 2 luật trên Công báo: chưa đọc, nên Điều 31–39 Luật 91/2025 và từ Điều 29 Luật Trí tuệ nhân tạo chỉ biết qua bản tin · chính sách bảo mật của OPA CRM, Xưởng Media, Creative Intelligence OS: không thấy link trên trang.
