# 60 kịch bản Văn Minh — đánh giá skill 04/24 + bản HeyGen talking-head

**Nguồn:** `60-kich-ban-video-ngan-ai-vm-dabest.md`  
**Skill dùng:** `04-script-video` (Mode B personal brand + QA 10 tiêu chí), `24-ai-avatar-production` (anti-detect, disclosure, QA 100), `25-voice-clone-podcast` (pause), runtime HeyGen v3.  
**Ngày:** 2026-08-26  
**Không render video trong bước này** — chưa chốt presenter (wolfgang / nbb / ảnh mới).

---

## 1. Kết luận ngắn

Bộ 60 kịch bản **đúng hướng personal brand** (hook kết quả, 1 CTA, không chào, có overlay).  
Nó **không phải** kịch bản HeyGen. Hầu hết là **quay màn hình + trước/sau + lưới ảnh**. Avatar talking-head **không** hiện được bóng đổ sai, lưới 9 góc, prompt cũ/mới, timelapse brand sheet.

| Câu hỏi | Trả lời |
|---|---|
| Có cuốn hút nếu quay người thật + B-roll? | Có — khung 04 đạt. |
| Đưa nguyên văn vào HeyGen? | Không — miệng nói, tay không chỉ được ảnh. |
| Skill 24 “nháy mắt / biểu cảm / ngắt nghỉ” có API riêng? | **Không có tool tên đó.** Đó là **anti-detect + pacing**, map sang engine/pause/SSML. |
| MCP gói 7138 (add-on 3569) làm được gì? | **Avatar III** = lipsync. **Không** `motion_prompt`, **không** `expressiveness`. Premium = 0 → IV/V fail. |

**Cách làm đúng:** mỗi video = **A-roll HeyGen (lời + pause)** + **B-roll CapCut** (ảnh, prompt, demo). Avatar III không thay editor.

---

## 2. Map “nháy mắt / biểu cảm / ngắt nghỉ” → HeyGen thật

Skill `24` §10 và `25` §Use case B nói **dấu hiệu + cách fix**, không phải nút trong API.

| Ý skill 24/25 | Engine / bề mặt | Cách ghi trong kịch bản |
|---|---|---|
| Mặt cứng, không nháy | Photo avatar + III yếu hơn digital twin / selfie video | Chọn **digital twin** (wolfgang) hoặc quay selfie train. III **không** có cờ “blink”. |
| Giọng đều, không ngắt | TTS mặc định | Câu ≤12–15 từ. Dấu chấm. SSML `<break time="0.35s"/>` nếu đi `create_speech` → `audio_url`. Trong `script` của `create_video_from_avatar`: **không SSML** — chỉ chấm/phẩy/dòng mới. |
| Chỉ miệng cử động | III không `motion_prompt` | III: chấp nhận talking-head tĩnh. IV/V: `motion_prompt` tiếng Anh + `expressiveness: medium`. MCP hiện **premium = 0** → đừng submit IV. |
| Micro-expression | IV `expressiveness` high/medium/low (photo) | Ghi note đạo diễn; chỉ gửi khi dùng IV/V. |
| Pause 1–2s sau câu quan trọng (`25`) | Speech SSML hoặc im lặng trong audio | Hook xong `0.4–0.6s`. Trước CTA `0.5s`. Không pad 2s chết — Video Agent sẽ bị dead air; Avatar III thì im miệng. |

**Hai đường render (chốt trước khi bấm):**

1. **Gói 7138 / MCP / Avatar III** — `script` thuần + overlay CapCut. Cử chỉ tay **không** điều khiển được.  
2. **Ví API / Avatar V** (đã smoke wolfgang 24s) — `motion_prompt` + digital twin. Đắt hơn, **không** trừ 7138.

Khi `avatar_id` đã set: **cấm** mô tả mặt/áo trong prompt. Chỉ nói “the selected presenter”.

**SSML mẫu (chỉ `create_speech`, `inputType=ssml`):**

```xml
<speak>
90% ảnh AI trông giả.
<break time="0.45s"/>
Không phải vì công cụ dở.
<break time="0.35s"/>
Bạn đang bỏ quên ánh sáng.
</speak>
```

`break` **phải giây** (`0.35s`), không dùng mili giây.

**Disclosure (24 + NĐ 147):** overlay 3s đầu hoặc cuối: `Video này dùng công nghệ AI Avatar`. Organic = tầng NÊN. Ads = BAT BUỘC.

---

## 3. QA cả bộ theo skill 04 (Mode B) + HeyGen

Thang: **PASS** ≥85 ý / **FIX** 70–84 / **HYBRID** cần B-roll mới sống / **KHÔNG III** nếu chỉ talking-head thì mất hook.

| # | Tên | 04 hook/1 ý | HeyGen thuần | Việc cần làm |
|---|---|---|---|---|
| 01 | Ảnh giả vì ánh sáng | PASS | HYBRID | A-roll + split before/after |
| 02 | 1 ảnh → 5 tài sản | PASS | HYBRID | Đếm 5 nhãn overlay; B-roll 5 output |
| 03 | Brief “đẹp và sang” | PASS | HYBRID | Gạch prompt trên B-roll |
| 04 | Catalogue → bán hàng | PASS | HYBRID | 2 ảnh cạnh nhau |
| 05 | Nhất quán bộ sưu tập | PASS | HYBRID | 6 ảnh lệch vs 3 ảnh khóa |
| 06 | Moodboard 1 câu | PASS | HYBRID | Lưới moodboard |
| 07 | Ảnh người thật làm gốc | PASS | HYBRID | Face lock demo |
| 08 | 9 góc máy | PASS | HYBRID | Lưới 3×3 — **không** tả bằng miệng |
| 09 | QC không nói dối | PASS | HYBRID | Khoanh chi tiết bịa |
| 10 | Upscale sau | PASS | HYBRID | UI credits — **không bịa số credits** |
| 11 | Brand sheet 1 buổi | FIX (dài, 7 beat) | HYBRID | Rút 45s; timelapse B-roll |
| 12 | Thử thách 10 phút | PASS | HYBRID | Đồng hồ + ảnh gốc |
| 13 | Ảnh → video QC | PASS | HYBRID | Cắt ảnh→video ngay frame 0 |
| 14 | 3 lỗi video AI | PASS | HYBRID | 3 clip lỗi |
| 15 | 3 chuyển động máy | PASS | HYBRID | 3 take |
| 16 | UGC không studio | PASS | HYBRID | 2 UGC |
| 17 | KOL ảo nhất quán | PASS | HYBRID | Bộ neo 4 góc |
| 18 | Thoại như brochure | **PASS talking-head** | A-roll mạnh | Ưu tiên HeyGen |
| 19 | Storyboard 5 cảnh | PASS | HYBRID | 5 khung |
| 20 | 15s có nhịp | PASS | HYBRID | Timeline đè hình |
| 21 | AI edit footage thật | PASS | HYBRID | Footage thô |
| 22 | Ảnh→video không bay | PASS | HYBRID | Clip méo |
| 23 | F&B | PASS | HYBRID | Texture món |
| 24 | KOL ảo vs người thật | **PASS talking-head** | A-roll | Split screen B-roll nếu có |
| 25 | Đừng đổi model | **PASS talking-head** | A-roll + 3 ảnh lỗi | |
| 26 | Chữ trong ảnh AI | PASS | HYBRID | Zoom chữ sai |
| 27 | 1 prompt 3 kết quả | PASS | HYBRID | 3 output |
| 28 | AI tự viết prompt | PASS | HYBRID | Prompt trên màn |
| 29 | Tool mới có đáng | FIX (placeholder) | HYBRID | Phải có tool + ngày test |
| 30 | Prompt quá dài | PASS | HYBRID | Prompt đầy màn |
| 31 | Khi nào không dùng AI | **PASS talking-head** | A-roll | |
| 32 | Đẹp nhưng vô dụng | PASS | HYBRID | Video mẫu |
| 33 | Free vs trả phí | FIX (cần test thật) | HYBRID | Không gắn nhãn thắng khi chưa test |
| 34 | AI hiểu văn hóa Việt | PASS | HYBRID | Lỗi cụ thể (phở, áo dài…) |
| 35–42 | Tin AI | FIX format | HYBRID | **Thiếu [TIN] [NGÀY] [NGUỒN] = không quay** |
| 43–50 | Cộng đồng | PASS ý | HYBRID | Cần bài học viên + consent |
| 51 | Đừng mua khóa nếu chưa biết đầu ra | **PASS talking-head** | A-roll | |
| 52 | Không dạy xem AI | PASS | HYBRID | 5 output |
| 53 | Tool vs workflow | **PASS talking-head** | A-roll | |
| 54 | 7 ngày | PASS | HYBRID | Lịch + output |
| 55 | DN không cần 20 tool | PASS | HYBRID | Sơ đồ rối |
| 56 | Case team MKT | FIX | HYBRID | **Case phải có thật / xin phép** |
| 57 | Portfolio | PASS | HYBRID | Trang portfolio |
| 58 | Credits | PASS | A-roll + UI | Không bịa số dư |
| 59 | Khóa không dành cho ai | **PASS talking-head** | A-roll | |
| 60 | 60 ngày: lưu vs thư viện | **PASS talking-head** | HYBRID nhẹ | Folder tài sản |

**Điểm yếu lặp lại (Gate 2 skill 04):**

1. Claim **“90%”** (video 01) không nguồn → đổi thành quan sát (“phần lớn ảnh mình chấm”).  
2. Video 11, 17, 54 nhồi **>3 beat**.  
3. 35–42 chưa phải kịch bản — mới là khuôn.  
4. 56/47/44: social proof **cần người + phép**. Không bịa học viên.  
5. Nhiều câu >15 từ, văn viết.  
6. Hook **visual bắt buộc** (04 §3 lớp) — talking-head thuần **trượt** nếu không có chữ lớn + B-roll 0–1s.

**Viral score thô (04):** demo 01–08, 13–14 ≈ 18–22/25 nếu có B-roll. Talking-head thuần không B-roll ≈ 12–16 (yếu visual hook).

---

## 4. Quy tắc lời thoại HeyGen (áp mọi video)

Viết **cho tai**, không cho trang giấy.

1. Một video = **một ý**.  
2. Câu **≤ 15 từ**. Câu hook **≤ 12 từ**.  
3. Không mở “Xin chào”. Mode B được mở bằng thất bại/quan sát, không CV.  
4. Số đọc thành lời (“chín góc”), overlay ghi số (“9 góc”).  
5. **Một CTA**, một keyword.  
6. Overlay ≤ 50 ký tự / dòng, có mặt từ giây 0 (tắt tiếng vẫn hiểu).  
7. Nhịp: `câu ngắn — break 0.3–0.5s — câu trả giá`.  
8. Biểu cảm ghi **tiếng Anh** (engine), lời **tiếng Việt**.  
9. III: cột biểu cảm = “auto lipsync / slight head from engine”. Không hứa tay chỉ.  
10. B-roll ≤5s skill Video Agent cấm; **CapCut thì 1–2s cut được**.

**Bảng đạo diễn biểu cảm (dùng khi IV/V):**

| Beat | motion_prompt (EN) | Cảm giác |
|---|---|---|
| Hook | Lean in 5cm, brows up on first stress word, one blink after first sentence | Đâm vào |
| Proof | Small nod, left hand chop once (keep in frame) | Chốt |
| Teach | Relax shoulders, slower blink, look at camera not down | Dạy |
| Twist | Head tilt right, pause, then nod | Lật |
| CTA | Lean back 3cm, open palm, hold last line | Mời |

**III:** cùng bảng chỉ để **diễn viên người thật** hoặc **bỏ**. Đừng nhét vào `script`.

---

## 5. Bản viết lại ưu tiên (full HeyGen pack)

Tám video **nên làm trước** trên avatar: vừa A-roll khỏe, vừa ít phụ thuộc demo. Mỗi pack: overlay, VO, SSML, B-roll bắt buộc, motion (IV/V), CTA.

### Video 18 — Lời thoại như brochure (A-roll mạnh nhất)

**Vì sao lên trước:** skill 04 Mode B + đúng nỗi đau talking-head.  
**Thời lượng VO:** ~22s nói + B-roll 8–12s = 35–40s.

| Lớp hook | Nội dung |
|---|---|
| Visual | Hai dòng thoại: brochure vs đời thường, gạch đỏ dòng 1 |
| Audio | “Video AI của bạn không giả vì hình.” |
| Text | `Giả vì đang nói như catalogue` |

**VO (III `script`):**

```
Video AI của bạn không giả vì hình.
Nó giả vì nhân vật đang nói như catalogue.
“Sản phẩm mang đến giải pháp tối ưu.”
Khách không nói vậy.
Khách nói: tôi mất cả buổi vì việc này.
Từ khi làm thế này, tôi xong trước giờ cơm.
Đổi lời trước khi đổi model.
Bình luận UGC THOẠI. Mình gửi khung ba câu.
```

**SSML (`create_speech`):**

```xml
<speak>
Video AI của bạn không giả vì hình.
<break time="0.4s"/>
Nó giả vì nhân vật đang nói như catalogue.
<break time="0.55s"/>
Sản phẩm mang đến giải pháp tối ưu.
<break time="0.35s"/>
Khách không nói vậy.
<break time="0.3s"/>
Khách nói: tôi mất cả buổi vì việc này.
<break time="0.25s"/>
Từ khi làm thế này, tôi xong trước giờ cơm.
<break time="0.45s"/>
Đổi lời trước khi đổi model.
<break time="0.4s"/>
Bình luận UGC THOẠI. Mình gửi khung ba câu.
</speak>
```

**Overlay lần lượt:** `Không giả vì hình` → `Đang nói như catalogue` → `UGC THOẠI`  
**B-roll:** 2 take thoại (cứng / tự nhiên).  
**Motion IV/V:** lean in on “không giả vì hình”; slight grimace on brochure line; nod on CTA.  
**Disclosure:** cuối, chữ nhỏ.

---

### Video 01 — Ảnh giả vì ánh sáng (HYBRID)

**Sửa claim:** bỏ “90%” không nguồn.

| Lớp | Nội dung |
|---|---|
| Visual | Split bóng sai / bóng đúng, 0–1s |
| Audio | “Ảnh AI trông giả thường không phải vì tool dở.” |
| Text | `Sai một thứ: hướng sáng` |

**VO:**

```
Ảnh AI trông giả thường không phải vì tool dở.
Bạn đang bỏ quên ánh sáng.
Bên này sáng từ phải. Bóng lại đổ sang phải.
Mắt người bắt lỗi ngay. Dù không gọi được tên.
Đừng ghi “sang trọng”.
Ghi nguồn sáng, hướng bóng, chất liệu, tiêu cự.
Bình luận ÁNH SÁNG. Mình gửi khung prompt.
```

**SSML:** break 0.4s sau câu 1; 0.5s sau “bỏ quên ánh sáng”; 0.35s trước CTA.  
**B-roll bắt buộc:** pair ảnh; zoom bóng; prompt cũ vs mới.  
**Motion:** brow up “giả”; chop “nguồn sáng, hướng bóng”.  
**QA 04:** ~88 nếu có split ngay frame 0; ~72 nếu chỉ mặt nói.

---

### Video 03 — Brief “đẹp và sang”

**VO:**

```
Brief “làm đẹp, sang, cao cấp” là lý do bạn nhận mười ảnh khác nhau.
AI không thiếu tưởng tượng.
AI thiếu tiêu chí để chấm.
Năm dòng: khách, sản phẩm, cảm xúc, màu, góc máy.
Rồi mới viết prompt.
Cùng một sản phẩm. Brief rõ thì lặp lại được.
Bình luận BRIEF. Nhận mẫu năm dòng.
```

**Overlay:** `Đẹp + sang = 10 ảnh lệch` → `5 dòng brief` → `BRIEF`  
**B-roll:** gạch đỏ prompt; gõ 5 dòng.

---

### Video 14 — Ba lỗi video AI

**VO:**

```
Ba lỗi khiến người xem mất tin video AI trong năm giây.
Một: tay cử động nhưng không có lực.
Hai: chữ và logo bị vẽ lại.
Ba: ánh sáng đổi giữa các khung.
Đừng hỏi đẹp không.
Hỏi: người xem có tin không.
Gửi một lỗi bạn hay gặp. Mình làm phần hai.
```

**B-roll:** 3 đoạn lỗi, mỗi đoạn ≤2s.  
**Không** để avatar “diễn” tay sai — đó là footage lỗi, không phải motion_prompt.

---

### Video 25 — Đừng đổi model

**VO:**

```
Kết quả xấu không có nghĩa bạn cần model mới.
Brief vẫn mơ hồ thì đổi tool chỉ đổi kiểu thất vọng.
Giữ nguyên tool.
Sửa chủ thể, bối cảnh, góc máy, ánh sáng, mục tiêu.
Biến số lớn nhất thường là brief. Không phải model.
Bình luận BRIEF TRƯỚC TOOL nếu bạn từng đổi tool vì ảnh xấu.
```

---

### Video 31 — Khi nào không dùng AI

**VO:**

```
Có việc tôi không dùng AI. Dù AI làm được.
Giá, pháp lý, ngày hết hạn: không để AI bịa số.
Testimonial chưa có khách thật: không dựng.
Đặc tính sản phẩm phải đúng: không phóng size, không thêm thành phần.
AI làm nháp. Người chịu trách nhiệm vẫn phải duyệt.
Bạn muốn list “nên / không nên” cho ngành nào?
```

**Mode B:** được dùng “tôi”. Overlay: `Không phải lúc nào cũng AI`.

---

### Video 51 — Đừng mua khóa nếu chưa biết đầu ra

**VO:**

```
Đừng mua khóa AI nếu bạn chưa biết mình muốn làm ra cái gì.
Ảnh sản phẩm nào. Video nào. Cho ai dùng.
Khóa học đi theo đầu ra. Không đi theo danh sách tool.
Bình luận MỤC TIÊU. Nhận worksheet tự hỏi trước khi đóng tiền.
```

**Không** hứa việc làm / doanh thu.

---

### Video 59 — Khóa không dành cho ai

**VO:**

```
Nói thẳng. Khóa này không dành cho người chỉ muốn xem vài clip AI rồi chờ viral.
Không hợp nếu bạn không muốn làm bài, không muốn sửa, chỉ tìm tool kiếm tiền nhanh.
Hợp SME, marketer, freelancer. Người cần ảnh và video dùng được.
Muốn làm thật: bình luận LÀM THẬT.
```

---

## 6. Pack rút gọn — phần còn lại (VO + overlay + B-roll tối thiểu)

Chỉ **lời avatar**. Demo để trong cột B-roll. Câu đã cắt ≤15 từ.

### Phần I — 02, 04–12

**02 — Năm tài sản**  
VO: `Một ảnh gốc. Năm tài sản. Vẫn đúng sản phẩm. Hero. Lifestyle. Cận chất liệu. Video. Banner. Không phải tạo nhiều. Là giữ màu và form. Bình luận 5 TÀI SẢN.`  
Overlay: `1 ảnh → 5 tài sản`  
B-roll: 5 output dán nhãn.

**04**  
VO: `Ảnh nền trắng nói sản phẩm tồn tại. Ảnh bán hàng cho khách hình dung lúc dùng. Tôi không để AI phát minh sản phẩm. Chỉ đổi bối cảnh và sáng. Gửi ngành hàng. Mình làm demo.`  
B-roll: trắng vs lifestyle.

**05**  
VO: `Mỗi ảnh một thương hiệu khác thì khóa ba thứ. Palette. Nguồn sáng. Cách đặt sản phẩm. Nhất quán không tới từ may. Tới từ tiêu chí lặp. Bình luận NHẤT QUÁN.`  
B-roll: 6 lệch → 3 khóa.

**06**  
VO: `Đừng bắt đầu brand bằng logo. Bắt đầu bằng cảm giác. Một câu “tự nhiên nhưng hiện đại” thành moodboard: màu, chất liệu, sáng, kiểu ảnh. Designer và AI cùng một hướng. Bình luận MOODBOARD.`  
B-roll: 5 ô moodboard.

**07**  
VO: `Muốn ảnh AI bớt giả, đừng bắt AI làm từ số không. Ảnh thật đã có da, sáng, dáng. Tôi chỉ đổi phông và đạo cụ. Giữ thông tin tốt là kỹ năng. Bình luận ẢNH GỐC.`  
B-roll: face lock.

**08**  
VO: `Một ảnh. Chín góc. Dưới một phút. Chính diện, bốn lăm độ, cận, top-down, profile, lifestyle, low angle, over-shoulder, hero. Rồi loại góc không hợp sản phẩm. Bình luận 9 GÓC.`  
B-roll: lưới 3×3 **bắt buộc**.

**09**  
VO: `AI được đổi sáng, cảnh, bố cục. Không được đổi size, công dụng, thành phần. Ảnh đẹp để khách dừng. Ảnh sai để mất tin. Bạn để ranh giới ở đâu? Bình luận TRUNG THỰC.`  
B-roll: khoanh chi tiết bịa.

**10**  
VO: `Đừng upscale ảnh bạn chưa chắc dùng. Nháp vừa đủ. Chọn một. Rồi mới nâng nét. Tiết kiệm không phải làm ít. Là chỉ đầu tư bản sẽ đăng. Bình luận CREDITS.`  
Không đọc số credits bịa.

**11** (rút beat)  
VO: `Brief ba dòng. Brand sheet trong một buổi. Không bắt đầu bằng logo. Bắt đầu bằng khách, cảm giác, lúc dùng. AI nháp nhanh. Người chọn và sửa. Bình luận BRAND SHEET.`  
B-roll: timelapse 8–10s, không 7 beat nói.

**12**  
VO: `Sản phẩm bình thường. Mười phút. Làm đáng dừng hơn. Không được nói dối. Đối tượng, hành động, cảm xúc. Không biến hàng thành thứ lạ. Cho khách thấy đúng cảnh dùng. Comment ngành hàng.`  
B-roll: clock 10:00.

### Phần II — 13, 15–17, 19–24

**13** VO: `Một ảnh tĩnh. Thành video tiếng Việt. Ảnh gốc. Một câu chuyển động. Lời mười giây. Bản nháp thôi. Kiểm tra logo, tay, chữ. Bình luận ẢNH THÀNH VIDEO.`  
**15** VO: `Cùng một ảnh. Ba máy. Dolly-in thì cao cấp. Orbit thì khám phá. Handheld thì đời. Dễ lỗi. Một video ngắn: một chuyển động. Bình luận CAMERA.`  
**16** VO: `UGC không bắt đầu bằng máy đắt. Bắt đầu bằng tình huống đúng. Ai dùng. Lúc nào. Xong việc gì. AI dựng cảnh. Kịch bản vẫn từ nỗi đau khách. Bình luận UGC.`  
**17** VO: `Tạo KOL ảo dễ. Giữ giống ở video thứ mười mới khó. Cần bộ neo: chính diện, nghiêng, toàn thân, mặt, đồ chuẩn. Đừng random từng cảnh. Bình luận KOL ẢO.`  
**19** VO: `Đừng bảo AI làm một video. Bảo nó chia thành khoảnh khắc có mục đích. Vấn đề. Sản phẩm. Cách dùng. Bằng chứng. CTA. Cảnh đẹp mà không dẫn chuyện thì cắt. Bình luận STORYBOARD.`  
**20** VO: `Mười lăm giây không ngắn. Nó không cho nói lan man. Ba giây vấn đề. Năm giây sản phẩm. Năm giây bằng chứng. Hai giây CTA. Mỗi cảnh một việc. Bình luận 15 GIÂY.`  
**21** VO: `Một footage thô. AI edit. Nó giỏi cắt lặng, nhịp, phụ đề. Người vẫn sửa câu, cảm xúc, logo. AI editor vòng một. Bạn editor cuối. Bình luận TEST THẬT.`  
**22** VO: `Muốn sản phẩm đứng, camera chạy? Nói rõ. Không thì cả hai cùng bay. Khóa chủ thể. Khóa form. Chỉ định phần được chuyển. Bình luận CHUYỂN ĐỘNG.`  
**23** VO: `Quán không cần điện ảnh. Cần video khiến khách đói đúng lúc. Texture. Góc cận. Hơi nóng. Tay gắp. Không claim dinh dưỡng nếu chưa có. Bình luận F&B.`  
**24** VO: `KOL ảo không luôn rẻ hơn người thật. Bạn cần loại tin nào. Ảo: nhiều phiên bản, kiểm soát hình. Thật: trải nghiệm, uy tín. Đừng dùng AI giả trải nghiệm chưa có. Bạn chọn gì?`

### Phần III — 26–34

**26** VO: `Chữ trong ảnh AI đẹp ư. Phóng to rồi hãy đăng. Nền để AI. Chữ giá ngày tháng: tool thiết kế. Bình luận nếu từng dính chữ sai.`  
**27** VO: `Cùng prompt. Ba ảnh khác nhau. Prompt là hướng dẫn. Không phải hợp đồng. Có ảnh neo. Có tiêu chí loại. Có vòng chọn-sửa. Bình luận BIẾN ĐỘNG.`  
**28** VO: `Tôi tả sản phẩm đời thường. Để AI viết prompt. Nó đúng phần mô tả. Nó thừa mỹ từ. Vẫn phải đạo diễn. Gửi một câu đời thường.`  
**29** Chỉ quay khi có tên tool + ngày + 4 tiêu chí test. Không viết VO generic.  
**30** VO: `Prompt dài không tự thành prompt tốt. Bốn tầng: chủ thể, bố cục, sáng, ràng buộc. Ưu tiên rõ, AI ít đoán. Bình luận 4 TẦNG.`  
**32** VO: `Video này đẹp. Tôi là khách, tôi chưa biết mua gì. Có hình, nhạc, chuyển động. Thiếu đối tượng, lợi ích, hành động. Gửi clip đẹp mà khó hiểu.`  
**33** Cấm kết luận “trả phí thắng” khi chưa test cùng prompt.  
**34** VO: `Brief rất Việt. Bản đầu sai đúng chỗ văn hóa. AI hiểu từ khóa. Chưa chắc hiểu bối cảnh. Cần ảnh neo và người Việt duyệt. Gửi một cảnh Việt để thử.`

### Phần IV — 35–42 (khuôn, chưa kịch bản)

Mỗi tập **bắt buộc** điền: tin, ngày, nguồn, “nên nếu / chưa nếu”.  
Khuôn VO:

```
[Headline]. Cập nhật [ngày], nguồn [tên].
Một câu: nó làm được gì.
SME nên dùng nếu [điều kiện].
Chưa cần nếu [điều kiện].
Bình luận ngành hàng. Mình test case thật.
```

Thiếu nguồn → **không render**.

### Phần V — 43–50

Cần bài thật + consent. VO khung:

**43** `Tôi không chấm “đẹp”. Bốn tiêu chí: đúng brief, nhất quán, dùng được, lặp lại được. Hashtag BAILAMTHAT.`  
**44** Chỉ khi có học viên thật.  
**45** `Bài 15 phút. Một ảnh quảng cáo. Đối tượng, cảm xúc, góc máy. Tự chấm rồi nộp.`  
**46** `Prompt này không tệ. Nó bắt AI đoán nhiều thứ. Chủ thể, cảnh, góc, ràng buộc.`  
**48** `Một ảnh. Bảy ngày. Bảy tài sản. Hero, lifestyle, cận, banner, video, UGC, brand sheet.`  
**49** `Ba lần AI sai: méo hàng, sai màu, chữ lỗi. Sửa lỗi cũng là năng lực.`  
**50** `Cộng đồng chỉ có người xem thì chưa phải chỗ học AI. Cần bài, hạn, feedback.`

### Phần VI — 52–58, 60

**52** VO: `Khóa này không dạy ngồi xem AI. Bắt làm ra năm tài sản dùng được. Ai chưa muốn làm bài thì chưa hợp.`  
**53** VO: `Công cụ biến mất, bạn còn biết cách làm không. Brief, ảnh gốc, prompt, tạo, kiểm, sửa. Tool đổi. Workflow mới là tài sản. Bình luận WORKFLOW.`  
**54** VO: `Bảy ngày không biến bạn thành chuyên gia. Cần một tài sản dùng được. Đây là thực hành. Không phải cam kết doanh thu. Bình luận 7 NGÀY.`  
**55** VO: `Doanh nghiệp không cần nhân viên thuộc 20 tool. Cần một workflow chạy. Brief, brand sheet, prompt, batch, duyệt. Chủ DN bình luận ĐÀO TẠO TEAM.`  
**56** **HOLD** đến khi có case xin phép.  
**57** VO: `Đừng nói “biết AI”. Cho khách xem đã làm gì. Một sản phẩm. Một video. Một workflow. Ghi phần AI, phần người. Không bịa case. Bình luận PORTFOLIO.`  
**58** VO: `Bấm thử lung tung thì credits hết trước khi ra năng lực. Nháp trước. Prompt có xương. Chỉ upscale bản đăng. Bình luận TIẾT KIỆM.`  
**60** VO: `Sáu mươi ngày tới: tiếp tục lưu video, hoặc bắt đầu thư viện tài sản của mình. Không ai bán prompt thành công hộ bạn. Workflow tốt cho ra sản phẩm thật. Workshop: link bio. Team: nhắn TEAM AI.`

---

## 7. Hàng sản xuất HeyGen (khi đã chốt mặt)

1. Chọn presenter (wolfgang / nbb / ảnh mới).  
2. Chọn túi: MCP **III** (7138 UI / 3569 API add-on) **hoặc** ví API **V**. Không trộn.  
3. Lấy pack VO + overlay từ file này.  
4. III: `create_video_from_avatar` + `engine.avatar_iii` + `script`. Overlay/B-roll trong CapCut.  
5. Muốn pause chuẩn: `create_speech` SSML → `audio_url` → video (vẫn III nếu gói).  
6. IV/V chỉ khi premium/ví đủ; gắn `motion_prompt` cột trên.  
7. QA 24: lipsync, pause, overlay disclosure, CTA một keyword.  
8. Không publish ads nếu chưa overlay AI.

**Ưu tiên render 8 clip:** 18 → 01 → 03 → 14 → 25 → 31 → 51 → 59.

---

## 8. Việc skill 04 còn thiếu trên bản gốc (không sửa trong file này)

- Chưa có 2 variant A/B / video.  
- Chưa viral score từng tập.  
- Chưa khối bàn giao quay (nhạc, đèn, subtitle).  
- Chưa Gate 2 nguồn số.  
Khi làm từng tập “đăng tuần này”, viết thêm variant B (hook khác) theo 04.

---

## Next

Chốt **một** presenter + **III gói** hay **V ví API**. Nói số video (ví dụ “render 18”). Lúc đó mới gọi MCP/CLI.
