---
name: opa-content-os
description: Hệ thống 16 AI Agent tự động hóa sản xuất nội dung đa kênh chuẩn LinTech Content OS tích hợp tiêu chuẩn OPA.
version: 1.0.0
author: OPA Operator
license: MIT
metadata:
  hermes:
    tags: [content-os, 16-ai-agents, marketing, social-media, video-production, quality-gate]
---

# OPA Content OS — Hệ Thống 16 AI Agent Vận Hành Nội Dung Đa Kênh

Mô hình nhà máy nội dung tự động hóa bán phần (Semi-autonomous Content Factory) với nguyên tắc **Human-in-the-Loop 3 điểm chạm**.

---

## Kiến trúc Tổng thể (16 Agents across 4 Stages)

```
[Google Sheet / DB: Brand Brain + Chiến lược]
                     │
                     ▼
┌────────────────────────────────────────────────────────┐
│ CHẶNG 1: LÊN PLAN & Ý TƯỞNG                            │
│  - Agent 1: Nghiên cứu & Radar (Research & Radar)      │
│  - Agent 2: Lập Kế hoạch Tuần (Content Planner)        │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
          [CỔNG 1: DUYỆT PLAN (Human Gate 1)]
          (Con người duyệt chủ đề & angle trên Sheet)
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│ CHẶNG 2A: DÂY CHUYỀN CHỮ │  │ CHẶNG 2B: VIDEO & VISUAL │
│ - Agent 3: Dàn ý         │  │ - Agent 9: Kịch bản video│
│ - Agent 4: Viết bài      │  │ - [CỔNG 2: QUAY RAW CLIP]│
│ - Agent 5: Duyệt bài (<8)│  │ - Agent 10: Dựng video   │
│ - Agent 6: Kiểm chứng    │  │ - Agent 11: Duyệt video  │
│ - Agent 7: Nhân bản (Thr)│  │ - Agent 12: Ảnh bìa      │
│ - Agent 8: Carousel      │  │ - Agent 13: Duyệt ảnh bìa│
└─────────────┬────────────┘  └─────────────┬────────────┘
              └────────────┬────────────────┘
                           ▼
          [CỔNG 3: DUYỆT TRẠM CUỐI (Human Gate 3)]
          (Phiếu tổng hợp Telegram/Sheet: Approve / Note)
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ CHẶNG 3: XUẤT BẢN & TƯƠNG TÁC                          │
│  - Agent 14: Đăng bài đa kênh (Multi-channel Publisher)│
│  - Agent 15: Chăm sóc bình luận & DM (Community Agent) │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ CHẶNG 4: VÒNG HỌC TUẦN & TỐI ƯU                        │
│  - Agent 16: Phân tích số liệu & Cập nhật Brand Brain │
└────────────────────────────────────────────────────────┘
```

---

## Chi tiết Chặng 1: Lên Kế hoạch & Ý tưởng

Mục tiêu chặng 1: Tự động quét thị trường, chọn lọc góc tiếp cận và lên lịch bài viết cho tuần mới, không để người sáng tạo rơi vào bế tắc "hôm nay đăng gì".

---

### Agent 1 — Nghiên cứu & Radar (Research & Radar Agent)

- **Mục tiêu:** Quét các nguồn tin tức, bắt xu hướng mới nổi, phân tích nội dung thắng của đối thủ và bóc tách insight của tệp khán giả mục tiêu.
- **Tần suất kích hoạt:** Hằng ngày (07:00 sáng) hoặc kích hoạt thủ công trước phiên lập kế hoạch tuần.
- **Đầu vào (Input Contract):**
  - Danh sách kênh đối thủ / chuyên gia cùng ngành (TikTok handles, YouTube channels, X accounts).
  - RSS feeds / nguồn tin công nghệ (ArXiv, TechCrunch, HackerNews, ProductHunt).
  - Hồ sơ khách hàng mục tiêu (ICP) & Nỗi đau cốt lõi (Core Pains).
- **Quy trình thực thi:**
  1. Quét top 20 bài viết / video có tương tác đột biến trong 7 ngày qua của ngành.
  2. Bóc tách Hook và Format của các nội dung thắng (Winning angles).
  3. Đối chiếu với nỗi đau của tệp khách hàng: "Người học AI nhưng không áp dụng được thực tế, ngợp công cụ, cần quy trình chuyển đổi thành kết quả".
  4. Lọc bỏ tin tức rác hoặc giật tít vô bổ (No-hype filter).
- **Đầu ra bắt buộc (Output Contract - JSON):**
  ```json
  {
    "scan_timestamp": "YYYY-MM-DDTHH:MM:SSZ",
    "trends": [
      {
        "trend_id": "T01",
        "topic": "Xây dựng AI Agent thay vì học vẹt prompt ChatGPT",
        "source_type": "competitor_viral | industry_news | audience_pain",
        "evidence_url": "https://...",
        "audience_pain_point": "Biết prompt cơ bản nhưng không nối được thành quy trình tự động",
        "suggested_angles": [
          "Case study: Đội ngũ 1 người vận hành bằng 16 Agent",
          "Sai lầm: Mua prompt pack 500k vs Tự thiết kế hệ thống agentic"
        ],
        "hype_score": 2,
        "actionability_score": 9
      }
    ]
  }
  ```
- **Tiêu chí chấp nhận (Quality Gate):** Không có tin tức chung chung dạng "OpenAI vừa ra model mới" nếu không kèm góc nhìn "Doanh nghiệp / cá nhân ứng dụng vào đâu".

---

### Agent 2 — Lên Kế hoạch Tuần (Content Planner Agent)

- **Mục tiêu:** Chọn lọc từ dữ liệu của Agent 1, phân bổ đều theo các tầng phễu (TOFU/MOFU/BOFU), tạo lịch 5–7 bài viết cụ thể cho tuần mới.
- **Đầu vào (Input Contract):**
  - Dữ liệu `trends` đã lọc từ Agent 1.
  - KPI tuần và tỷ trọng nội dung (ví dụ: 40% TOFU - Nhận thức, 40% MOFU - Hướng dẫn quy trình, 20% BOFU - Chuyển đổi/Offer).
  - Lịch xuất bản cố định (Thứ 2 đến Chủ nhật, khung giờ vàng: 11h30 và 19h30).
- **Quy trình thực thi:**
  1. Phân bổ chủ đề vào ma trận 7 ngày.
  2. Định hình định dạng dự kiến cho từng bài (Bài viết Text dài, Video ngắn 60s, Chuỗi Threads, Slide Carousel).
  3. Soạn Brief chi tiết cho từng bài: Góc nhìn chính, Hook dự kiến, Giá trị trao đi (Takeaway), CTA mong muốn.
  4. Xuất dữ liệu trực tiếp vào Google Sheet / Bảng kế hoạch tuần.
- **Đầu ra bắt buộc (Output Contract - Format hàng Google Sheet):**
  | Ngày | Kênh ưu tiên | Định dạng | Angle / Chủ đề | Hook đề xuất | Phễu | Trạng thái duyệt |
  |---|---|---|---|---|---|---|
  | Thứ 2 | TikTok / FB | Video ngắn (60s) | Bóc tách Content OS 16 Agent | "Mình vừa tự động hóa 80% khâu làm content..." | TOFU | PENDING |
  | Thứ 3 | Threads / X | Text Thread | 5 lỗi khiến học AI mãi không ra tiền | "Lý do 90% người học AI bỏ cuộc sau 2 tuần:" | MOFU | PENDING |
  | Thứ 4 | FB / LinkedIn | Carousel 7 slide | Sơ đồ kiến trúc Human-in-the-Loop | "Tại sao không nên để AI tự đăng bài hoàn toàn?" | MOFU | PENDING |
  | Thứ 5 | TikTok / Shorts | Video ngắn (45s) | Show thực tế flow duyệt Telegram | "Đây là 3 nút mình bấm mỗi tuần để vận hành..." | BOFU | PENDING |
  | Thứ 6 | Toàn kênh | Bài viết sâu | Case study chuẩn hóa quy trình AI | "Hành trình biến 1 người thành phòng ban 5 người" | BOFU | PENDING |

---

### Cổng Duyệt 1: Hội Đồng Tự Duyệt Hoặc Duyệt Qua Chat (`GATE_1: COUNCIL_AUTO_APPROVED`)

- **Cơ chế mặc định (Zero-Babysitting Autonomous Council):**
  - Sau khi `agent-01` và `agent-02` lập 3 phương án (Tree of Thoughts), Hội đồng phản biện (`agent-05` + `agent-06`) tự chấm điểm, sửa tối thiểu 5 lỗi và nâng cấp lên `v2/v3` ($\ge 9.0/10$).
  - Ngay khi đạt $\ge 9.0/10$, Hội đồng tự cấp cờ `COUNCIL_AUTO_APPROVED` và **chuyển thẳng sang Chặng 2 (Thực thi toàn diện)** mà không bắt Anh Huy phải duyệt bản nháp thủ công.
- **Công nhận tuyệt đối chỉ đạo trên Chat:**
  - Mọi chỉ đạo hoặc xác nhận ngắn gọn của Anh Huy trên cửa sổ Chat (kể cả gõ nhanh/viết tắt) đều tương đương `PLAN_APPROVED` hợp lệ 100%, không bao giờ chờ phiếu Telegram ở Cổng 1.

---

## Chi tiết Chặng 2: Dây Chuyền Sản Xuất Đa Định Dạng

Chặng 2 phân thành 2 dây chuyền chạy song song độc lập dựa trên brief đã được duyệt ở Cổng 1.

---

### Chặng 2A: Dây Chuyền Sản Xuất Chữ & Định Dạng Tĩnh (Text Pipeline)

```
[Brief đã duyệt (APPROVED)]
            │
            ▼
   Agent 3: Lập Dàn Ý (Hook + Body + CTA)
            │
            ▼
   Agent 4: Viết Bản Thảo (Đúng Brand Voice)
            │
            ▼
   Agent 5: Duyệt Bài & Chấm Điểm (Score 0-10)
      ├── [Score < 8] ──> Viết lại (Max 2 vòng)
      └── [Score >= 8]
            │
            ▼
   Agent 6: Kiểm Chứng (Fact-check & Anti-hallucination)
            ├── Fail ──> Báo lỗi về Agent 4 sửa
            └── Pass
                 │
        ┌────────┴────────┐
        ▼                 ▼
   Agent 7:          Agent 8:
   Nhân Bản Threads  Thiết Kế Carousel
```

#### Agent 3 — Lập Dàn Ý (Outliner Agent)
- **Mục tiêu:** Bẻ nhỏ brief thành cấu trúc khung logic 3 phần rõ ràng, tối ưu tỷ lệ đọc hết bài.
- **Đầu vào:** Hàng brief `APPROVED` từ Google Sheet.
- **Quy trình:**
  1. Tạo 3 phương án Hook khác nhau: (1) Tò mò / Trái ngược nhận thức; (2) Kết quả cụ thể con số; (3) Nỗi đau trực diện.
  2. Xây dựng 3 luận điểm cốt lõi phần Thân bài theo công thức: Thực trạng $\rightarrow$ Nguyên nhân gốc rễ $\rightarrow$ Giải pháp hành động cụ thể.
  3. Định hình Call to Action (CTA): Kêu gọi thảo luận, để lại comment nhận tài liệu hoặc hướng dẫn thử nghiệm.
- **Đầu ra:** Bản dàn ý cấu trúc (Outline Schema).

#### Agent 4 — Viết Bản Thảo (Copywriting Agent)
- **Mục tiêu:** Chấp bút bài viết hoàn chỉnh cho Facebook/LinkedIn/TikTok Caption theo đúng tôn chỉ Brand Voice OPA: Điềm đạm, Thực chiến, Không giật tít vô căn cứ, Không lạm dụng emoji/buzzword.
- **Đầu vào:** Dàn ý từ Agent 3 + Bộ quy chuẩn Brand Voice (`references/brand-voice.md`).
- **Quy tắc viết:**
  - Tuyệt đối không dùng cụm từ sáo rỗng: "Trong kỷ nguyên số bùng nổ...", "AI đang thay đổi thế giới một cách chóng mặt...".
  - Đi thẳng vào vấn đề: Nêu tình huống thực tế $\rightarrow$ Cách giải quyết $\rightarrow$ Quy trình từng bước.
  - Độ dài chuẩn: 600 – 1.000 từ cho bài phân tích sâu; 150 – 250 từ cho caption video.

#### Agent 5 — Duyệt Bài & Chấm Điểm (Quality Gate Agent)
- **Mục tiêu:** Đóng vai trò giám khảo độc lập (LLM Judge), chấm điểm bài viết dựa trên Rubric chuẩn 4 tiêu chí (thang điểm 10):
  1. **Brand Voice Match (0-3đ):** Giọng văn điềm đạm, không khoe mẽ, không sáo rỗng.
  2. **Actionability (0-3đ):** Độc giả đọc xong có làm theo được ngay không hay chỉ là lý thuyết suông?
  3. **Hook Power (0-2đ):** 2 câu đầu có giữ chân được người đọc không?
  4. **Structure & Clarity (0-2đ):** Câu văn ngắn gọn, ngắt dòng thoáng, dễ đọc trên di động.
- **Quy tắc lặp (Loop Contract):**
  - **Nếu Điểm < 8.0/10:** Trả về Agent 4 kèm lý do gạch đầu dòng rõ ràng. Agent 4 bắt buộc phải viết lại.
  - **Giới hạn cứng:** Tối đa 2 vòng lặp. Nếu sau 2 vòng vẫn trượt, gắn nhãn `NEEDS_HUMAN_REVIEW` và đưa vào hàng chờ kiểm tra thủ công.

#### Agent 6 — Kiểm Chứng (Fact-check & Anti-hallucination Agent)
- **Mục tiêu:** Rà soát toàn bộ bài viết để loại bỏ ảo giác, thông tin sai lệch hoặc trích dẫn không có thật.
- **Quy trình:**
  1. Trích xuất toàn bộ: Con số, tên công cụ, API endpoint, tên chuyên gia, nghiên cứu khoa học.
  2. Đối chiếu nguồn hoặc yêu cầu đường link kiểm chứng.
  3. Nếu phát hiện số liệu bịa đặt: Đổi thành mô tả định tính hoặc cảnh báo sửa đổi ngay.
- **Đầu ra:** Báo cáo xác minh: `PASSED` hoặc `FAILED` kèm vị trí dòng cần sửa.

#### Agent 7 — Nhân Bản Nền Tảng Ngắn (Repurposing Agent)
- **Mục tiêu:** Chuyển đổi bài viết dài đã được kiểm duyệt thành chuỗi bài Threads (3–5 post) và bài viết ngắn cho X/Twitter.
- **Quy tắc:**
  - Post 1: Hook mạnh mẽ + Tuyên ngôn chính + Đính kèm hình ảnh/sơ đồ.
  - Post 2–4: Mỗi post là 1 bước thực hành độc lập, súc tích (<280 ký tự).
  - Post 5: Tóm tắt bài học + CTA chuyển đổi (Comment/Link).

#### Agent 8 — Thiết Kế Carousel (Visual Post Agent)
- **Mục tiêu:** Chuyển bài viết thành kịch bản slide 5–7 trang cho Facebook Carousel, Instagram Carousel hoặc tài liệu PDF LinkedIn.
- **Cấu trúc Slide chuẩn:**
  - Slide 1: Bìa (Tiêu đề tương phản cao, định vị rõ ai nên đọc).
  - Slide 2: Vấn đề / Sai lầm phổ biến.
  - Slide 3–5: 3 bước hành động hoặc 3 thành phần của quy trình.
  - Slide 6: Kết quả trước & sau khi áp dụng.
  - Slide 7: Tóm tắt + CTA (Lưu lại / Chia sẻ).

---

### Chặng 2B: Dây Chuyền Sản Xuất Video & Visual (Video Pipeline)

```
[Brief đã duyệt (APPROVED)]
            │
            ▼
   Agent 9: Kịch Bản Video & Phiếu Quay (Shotlist 35-55s)
            │
            ▼
   [CỔNG 2: HUMAN QUAY CLIP THÔ (Thả file vào Drive/Folder)]
            │
            ▼
   Agent 10: Dựng Video Tự Động (VAD cut, Kinetic Sub, SFX)
            │
            ▼
   Agent 11: Duyệt Video (Thời lượng, Khớp sub, Audio LUFS)
      ├── Fail ──> Dựng lại (Max 1 lần)
      └── Pass
            │
   ┌────────┴────────┐
   ▼                 ▼
Agent 12:         Agent 13:
Tạo Ảnh Bìa       Duyệt Ảnh Bìa Vision QA (Typo, Safezone)
(3:4 & 9:16)         ├── Fail ──> Sinh lại (Max 2 vòng)
                     └── Pass
```

#### Agent 9 — Kịch Bản Video & Phiếu Quay (Video Scriptwriter Agent)
- **Mục tiêu:** Tạo kịch bản video ngắn (35–55 giây) và phiếu quay rõ ràng để người quay chỉ việc đọc theo máy nhắc chữ mà không phải nghĩ.
- **Quy chuẩn kịch bản:**
  - **0–3 giây (Hook):** Tuyên bố đảo ngược nhận thức hoặc đưa ra giải pháp ngay (VD: *"Đừng học prompt ChatGPT nữa, đây là cách xây đội AI tự làm việc cho bạn..."*).
  - **4–20 giây (Setup & Problem):** Nêu nhanh thực trạng nhức nhối.
  - **21–45 giây (Framework / Breakdown):** Trình bày 3 bước cụ thể (kèm gợi ý chèn màn hình minh họa).
  - **46–55 giây (CTA):** Kêu gọi bình luận từ khóa để nhận tài liệu/link.
- **Phiếu quay (Shotlist) bao gồm:** Góc quay (Chính diện), Nét mặt/Tông giọng (Điềm đạm, dứt khoát), Đạo cụ hiển thị (Màn hình điện thoại/máy tính).

#### Cổng Thực Thi 2: Quay Clip Thô (Human Execution Gate 2)
- **Người thực hiện:** Creator / Founder.
- **Hành động:** 
  1. Mở phiếu quay, nhìn ống kính, nói 1–2 lần theo kịch bản.
  2. Không cần cắt ghép, không cần lo vấp nhẹ (AI sẽ tự động lọc).
  3. Thả file thô (`.mp4` / `.mov`) vào thư mục `/inbox_raw_videos/` hoặc Google Drive được liên kết.

#### Agent 10 — Dựng Video Tự Động (Video Editor Agent)
- **Mục tiêu:** Xử lý hậu kỳ tự động clip thô thành video hoàn chỉnh sẵn sàng đăng tải.
- **Công nghệ nền tảng:** FFmpeg 9.x + Faster-Whisper + Remotion 9:16 Engine (hoặc CapCut Template API).
- **Quy trình xử lý:**
  1. **Voice Activity Detection (VAD):** Dùng Faster-Whisper phát hiện khoảng lặng >0.6 giây và tự động cắt gọt (Silence removal).
  2. **Kinetic Subtitle:** Tạo phụ đề nhảy chữ nổi bật từng từ, highlight từ khóa quan trọng bằng màu thương hiệu (Cam / Vàng / Xanh Neon).
  3. **Auto Framing:** Cắt khung hình về chuẩn 9:16 (1080x1920) lấy nét vào khuôn mặt người nói.
  4. **SFX & Sound Leveling:** Chèn âm thanh woosh/pop khi xuất hiện keyword; cân bằng âm thanh đạt chuẩn podcast/reels (-14 LUFS).

#### Agent 11 — Duyệt Video (Video QA Agent)
- **Mục tiêu:** Kiểm tra chất lượng kỹ thuật file video xuất xưởng.
- **Checklist tự động:**
  - Thời lượng: Bắt buộc từ 30 đến 59.9 giây (tối ưu cho thuật toán short-form).
  - Định dạng: Video codec H.264, Audio AAC, độ phân giải tối thiểu 1080x1920, 30fps.
  - Độ lệch phụ đề: Độ trễ phụ đề so với giọng nói không được lệch quá 150ms.
  - Nếu lỗi kỹ thuật: Kích hoạt render lại tối đa 1 lần.

#### Agent 12 — Thiết Kế Ảnh Bìa (Thumbnail Agent)
- **Mục tiêu:** Tạo ảnh bìa bắt mắt, đồng bộ nhận diện thương hiệu cho 2 kích thước chuẩn:
  - Tỷ lệ 3:4: Dành cho lưới trang chủ TikTok và Facebook feed.
  - Tỷ lệ 9:16: Dành cho Instagram Reels, YouTube Shorts tab.
- **Nguyên tắc thiết kế:** Chữ to, ngắn gọn (tối đa 5–7 từ), font đậm không chân (Bold Sans-Serif), màu chữ tương phản mạnh với nền.

#### Agent 13 — Duyệt Ảnh Bìa Bằng Vision (Vision QA Agent)
- **Mục tiêu:** Dùng mô hình Multimodal Vision (như Gemini/GPT-4o Vision) quét file ảnh bìa trước khi xuất bản.
- **Tiêu chí kiểm định:**
  1. **Lỗi chính tả (Typo check):** Đọc chữ trên ảnh đối chiếu với tiêu đề brief.
  2. **Vùng an toàn (Safe-zone check):** Đảm bảo chữ và yếu tố quan trọng không nằm ở 15% đáy ảnh (nơi TikTok để caption và âm thanh) hoặc 10% bên phải (nơi để nút Like/Share).
  3. **Tương phản & Nhận diện:** Chữ phải đọc được rõ ràng khi thu nhỏ về kích thước icon điện thoại.
  - Nếu vi phạm: Yêu cầu Agent 12 vẽ lại (tối đa 2 vòng lặp).

---

## Chi tiết Chặng 3: Duyệt Trạm Cuối & Xuất Bản

Chặng 3 là nút thắt kiểm soát cuối cùng đảm bảo tôn chỉ: **"Không gì tự lên mạng khi mình chưa xem"**.

---

### Cổng Duyệt 3: Phiếu Duyệt Trạm Cuối (Human Gate 3)

- **Người thực hiện:** Founder / Creator / Operator.
- **Giao diện nhận duyệt:** Bot Telegram (`@OPANotifierBot`) gửi 1 Card thông báo kèm preview đa phương tiện:
  - **Tên chủ đề:** Bóc tách Content OS 16 Agent.
  - **Link preview video:** `https://.../video_preview.mp4`
  - **Ảnh bìa 3:4 & 9:16:** Đính kèm trực tiếp.
  - **Bản thảo bài viết Facebook & Caption:** Xem toàn văn.
  - **Kịch bản Threads:** 4 tweet liên kết.
- **Cách thức thao tác:**
  - Bấm nút inline Telegram `[✅ PHÊ DUYỆT ĐĂNG]`: Kích hoạt Agent 14 lên lịch đăng.
  - Gõ phản hồi sửa (ví dụ: *"Đổi câu mở đầu: bỏ từ 'mình' thay bằng 'đội OPA'"*): Kích hoạt Agent tương ứng sửa và gửi lại preview trong 60 giây.
  - Bấm `[⛔ TẠM DỪNG / HỦY]`: Đưa vào lưu trữ, không đăng.

---

### Agent 14 — Đăng Bài Đa Kênh (Multi-channel Publisher Agent)

- **Mục tiêu:** Tự động điều phối và xuất bản nội dung tới đúng kênh, đúng khung giờ vàng đã cấu hình.
- **Tích hợp API trực tiếp:**
  - **TikTok Content Posting API:** Tải video lên, gắn title + hashtag + ảnh bìa.
  - **Facebook Graph API:** Đăng Facebook Reels & bài viết Fanpage.
  - **YouTube Data API v3:** Tải lên YouTube Shorts kèm thẻ tags.
  - **Threads API / X API v2:** Đăng chuỗi bài tự động (Thread chaining).
  - **Telegram Channel Webhook:** Đăng tóm tắt và link điều hướng về kênh chính.
- **Cơ chế an toàn (Fault Tolerance):**
  - Cơ chế tự động thử lại (Retry with exponential backoff) nếu API nền tảng gặp sự cố mạng (tối đa 3 lần).
  - Báo cáo trạng thái thành công (`PUBLISHED`) hoặc thất bại (`FAILED` + Error Log) về lại Google Sheet và Telegram.

---

### Agent 15 — Chăm Sóc Bình Luận & DM (Community & Engagement Agent)

- **Mục tiêu:** Tương tác với khán giả trong 24 giờ vàng đầu tiên sau khi đăng bài để tăng điểm thuật toán phân phối.
- **Quy trình phân loại & xử lý bình luận:**
  1. **Bình luận chứa từ khóa CTA (Lead Trigger):**
     - Khán giả comment: *"AGENT"*, *"QUY TRÌNH"*, *"SHEET"*.
     - Xử lý: Tự động like comment, reply công khai: *"Mình vừa gửi link tài liệu qua tin nhắn cho bạn rồi nhé!"*, đồng thời kích hoạt bot gửi link tài nguyên vào DM/Inbox.
  2. **Bình luận thắc mắc chuyên môn / Phản biện:**
     - Xử lý: Soạn câu trả lời sâu, logic, khiêm tốn dựa trên kho tri thức OPA (`references/`), trình duyệt nếu câu hỏi mang tính nhạy cảm.
  3. **Bình luận khen ngợi:**
     - Xử lý: Cảm ơn và đặt một câu hỏi mở để mồi họ tiếp tục thảo luận (tăng tỷ lệ tương tác 2 chiều).
  4. **Bình luận tiêu cực / Trolling / Spam link bẩn:**
     - Xử lý: Tự động ẩn comment chứa từ khóa spam, link độc hại hoặc vi phạm chính sách cộng đồng.

---

## Chi tiết Chặng 4: Vòng Học Tuần & Tối Ưu (Closed-Loop Learning)

Mục tiêu chặng 4: Biến toàn bộ dữ liệu hiệu suất của tuần cũ thành "trí thông minh tích lũy" cho tuần mới, giúp hệ thống càng chạy càng sắc bén.

---

### Agent 16 — Phân Tích Số Liệu & Cập Nhật Brand Brain (Analytics & Brain Updater)

- **Thời điểm kích hoạt:** 23:00 Chủ Nhật hàng tuần.
- **Đầu vào:**
  - Dữ liệu API phân tích từ TikTok Analytics, Meta Business Suite, YouTube Analytics.
  - Số lượng leads / inbox thu thập được từ Agent 15.
- **Quy trình phân tích:**
  1. **Xếp hạng nội dung:** Phân loại bài viết thành 3 nhóm:
     - Nhóm Thắng (Top 20%): Reach cao đột biến, tỷ lệ giữ chân video >45% tại giây thứ 3.
     - Nhóm Bình thường (60%): Đạt KPI trung bình.
     - Nhóm Thất bại (Bottom 20%): Drop-off cao ngay trong 3 giây đầu, không có tương tác.
  2. **Bóc tách A/B Testing Hook:**
     - So sánh hiệu quả giữa các dạng hook (Ví dụ: Hook "Nghịch lý" đạt tỷ lệ giữ chân 52% vs Hook "Hỏi đáp" chỉ đạt 28%).
  3. **Rút ra bài học quy tắc (Rule Extraction):**
     - Tạo ra các luật mới (New Insights): *"Khán giả phản hồi tốt nhất với video quay màn hình thao tác thật kèm số liệu; các video chỉ nói triết lý lý thuyết có tỷ lệ xem hết thấp"*.
  4. **Cập nhật Brand Brain:**
     - Ghi nhận các "Từ khóa thắng" vào danh sách ưu tiên của Agent 1 & Agent 2.
     - Bổ sung các "Từ cấm" (từ gây mất thiện cảm hoặc bị bóp tương tác) vào file Brand Voice.
- **Bàn giao (Handoff):**
  - Xuất báo cáo ngắn gọn 1 trang (Weekly Performance Memo) gửi Founder qua Telegram.
  - Tự động nạp bộ luật mới vào Agent 1 và Agent 2 để sáng thứ Hai tuần kế tiếp bắt đầu một chu kỳ nội dung thông minh hơn.

---

## Bảng Ma Trận Phân Vai 16 Agent

| ID | Tên Agent | Thuộc Chặng | Đầu Vào Chính | Đầu Ra Chính | Cơ Chế Kiểm Soát |
|---|---|---|---|---|---|
| **01** | **Research & Radar** | Chặng 1 | Nguồn tin, đối thủ, ICP | Danh sách trend & angle | Lọc hype, chỉ giữ actionable |
| **02** | **Content Planner** | Chặng 1 | Trend từ Agent 1, KPI tuần | Lịch 5-7 bài + Brief | **CỔNG 1: Human duyệt trên Sheet** |
| **03** | **Outliner** | Chặng 2A | Brief đã duyệt | Dàn ý 3 phần (Hook-Body-CTA) | Kiểm tra cấu trúc logic |
| **04** | **Copywriter** | Chặng 2A | Dàn ý Agent 3 + Brand Voice | Bản thảo bài viết hoàn chỉnh | Tuân thủ Brand Voice OPA |
| **05** | **Content Evaluator** | Chặng 2A | Bản thảo Agent 4 | Điểm 0-10 + Feedback | **Điểm < 8 trả về viết lại (max 2)** |
| **06** | **Fact-checker** | Chặng 2A | Bài viết đã đạt điểm | Báo cáo xác thực fact | Chặn hallucination số liệu/link |
| **07** | **Repurposer** | Chặng 2A | Bài viết đã kiểm chứng | Chuỗi Threads (3-5 post) | Giới hạn 280 ký tự/post |
| **08** | **Carousel Builder** | Chặng 2A | Bài viết đã kiểm chứng | Kịch bản Slide 5-7 trang | Tối ưu hiển thị mobile |
| **09** | **Video Scriptwriter**| Chặng 2B | Brief đã duyệt | Kịch bản 35-55s + Shotlist | Khóa Hook 3 giây đầu |
| **--** | **Human Execution**  | Chặng 2B | Kịch bản Agent 9 | Video raw clip | **CỔNG 2: Human quay clip thô** |
| **10** | **Video Editor**     | Chặng 2B | Raw clip + Script | Video 9:16 cắt VAD, sub, SFX | FFmpeg + Faster-Whisper |
| **11** | **Video QA**         | Chặng 2B | Video đã dựng | File MP4 chuẩn kỹ thuật | Check thời lượng <60s, lệch sub |
| **12** | **Thumbnail Creator**| Chặng 2B | Brief + Video | Ảnh bìa 3:4 và 9:16 | Font to, tương phản cao |
| **13** | **Vision QA**        | Chặng 2B | Ảnh bìa Agent 12 | Ảnh bìa đã duyệt | **Model Vision check typo & safezone** |
| **--** | **Human Final Gate** | Chặng 3  | Toàn bộ asset đã sản xuất | Lệnh duyệt / Ghi chú sửa | **CỔNG 3: Human duyệt trạm cuối** |
| **14** | **Multi Publisher**  | Chặng 3  | Nội dung đã duyệt trạm cuối | Trạng thái đăng đa kênh | Retry tự động, log lỗi API |
| **15** | **Community Agent**  | Chặng 3  | Comment & DM từ người xem | Phản hồi tương tác, gửi link | Lọc spam, đẩy chuyển đổi lead |
| **16** | **Analytics & Brain**| Chặng 4  | Số liệu 7 ngày các nền tảng | Luật mới + Báo cáo tuần | Cập nhật tự động vào Brand Brain |
