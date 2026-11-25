# PLAN — viết `edit.json`

Đây là chỗ phán đoán duy nhất của dây chuyền A-roll: nghe lời, chia thẻ phụ đề,
chọn chữ đập, bảng liệt kê, cỡ cảnh. **Agent chỉ viết một file: `edit.json`.**
Frame, mức tiếng, SFX, camera đều do code sinh ra từ file này — không sửa
component, không viết giây, không đặt số frame tay.

Tư duy dựng của bản 1.0.0 được giữ nguyên; chỉ đổi chỗ ở: mọi mốc thời gian
trước đây viết bằng giây nay viết bằng **chỉ số từ** trong `words.json`.

## 1. Vòng làm việc (tối đa 3 vòng)

1. Lệnh đầu của card (SKILL.md mục 1: `stage.py PLAN --task <id>`) — script sinh
   `propose_edit.json` (khung do code cắt sẵn) và in đường dẫn của nó cùng
   đường dẫn file này.
2. Chép `propose_edit.json` thành `edit.json`, rồi sửa: đặt hook, gộp/tách
   block theo câu, chọn hero, chọn style/color, thêm steps và cta, chỉnh shots.
   **Luôn dùng đường dẫn tuyệt đối in ở dòng NEXT** (thư mục dự án
   `…/<n>/edit-r<ver>/`) — thư mục làm việc của card là `…/<n>/`, một cấp trên
   dự án, nên ghi `edit.json` theo đường dẫn tương đối sẽ lạc ra ngoài.
3. Kiểm: chạy đúng lệnh ở dòng NEXT (`stage.py PLAN --check --task <id>`, đường
   dẫn tuyệt đối trong ngoặc kép) — chạy `validate_edit.py`. In `ĐẠT` và
   `RESULT: PASS` là xong card: gọi tool `kanban_complete` đúng như dòng NEXT
   (summary chép nguyên văn dòng `ĐẠT: …` và dòng `RESULT: PASS`, metadata =
   JSON dòng `METADATA`).
4. `FAIL` thì sửa đúng các mã lỗi được in ra rồi chạy lại lệnh ở dòng NEXT.
   **Tối đa 3 vòng.** Vòng thứ 3 vẫn FAIL thì stage.py in `BLOCK`: làm đúng
   NEXT (tool `kanban_block`, kind `needs_input`), chép nguyên văn danh sách lỗi
   vào comment — operator sẽ mở card a2 với model mạnh hơn. FAIL hay BLOCK thì
   **không** complete. Không tự sửa script, không tự đổi rules.

File vào (đều nằm trong thư mục dự án, do INTAKE ghi):

| File | Dùng để |
|---|---|
| `words.json` | `[{i, w, s, e, on}]` — `w` là chữ hiển thị, `on` là mốc nói thật |
| `pauses.json` | khoảng ngắt, nhịp ngắt có chủ đích (`designed_breaks`), độ dài |
| `meta.json` | số video, preset, độ khớp lời, các từ ASR còn đoán |
| `propose_edit.json` | khung block/shots hợp lệ sẵn, chép ra rồi sửa |
| `examples/edit.json` | bản mẫu thật (video 02) đã qua mọi cổng |

## 2. Schema `edit/1.1` — chỉ nhãn, không có giây

```jsonc
{
  "schema": "edit/1.1",
  "hook":  { "text": "20", "color": "warn", "hit_word": 7 },      // hoặc null
  "blocks": [
    { "id": "b02", "top": [5, 7], "hero": [7, 9], "bottom": null,
      "style": "stomp", "color": "warn", "accent": null, "display": {}, "reveal": false }
  ],
  "steps": { "title": "5 TÀI SẢN TỪ 1 ẢNH",
             "items": [ { "range": [28, 32], "label": "Hero cho website" } ] },   // hoặc null
  "shots": [ { "cut_at_word": 21, "s0": 1.18, "s1": 1.22, "x": 0.0, "y": -0.06 } ],
  "cta":   { "range": [147, 162], "label": "Bình luận", "keyword": "5 TÀI SẢN" }  // hoặc null
}
```

- Mọi `[a, b)` là **index từ trong `words.json`**, nửa mở: `[4, 6)` = từ 4 và 5.
- **Mọi khoá phải có mặt**, giá trị không dùng thì để `null` (khung
  `propose_edit.json` đã có sẵn đủ khoá). Không thêm khoá lạ, không viết giây.
- Cách đo dùng trong mọi luật dưới đây:
  - **độ dài block** = `e` của từ cuối − `s` của từ đầu;
  - **mốc một sự kiện** (nhãn đập, cú cắt, hook) = `on` của từ — onset thật;
  - shot đầu tiên là khung mở, không tính là cú cắt.

## 3. blocks — thẻ phụ đề ba tầng

Mỗi block là một thẻ: dòng nhỏ trên / **dòng hero** / dòng nhỏ dưới, cùng hiện
trên màn. Ba tầng ghép lại thành một câu hoặc một vế câu.

| Trường | Quy tắc |
|---|---|
| `top`, `bottom` | từ dẫn / từ đuôi, cỡ nhỏ; để `null` khi không có |
| `hero` | **2–5 từ mang nghĩa** (luận điểm, con số, từ khoá); ≤ ~18 ký tự thì chữ to nhất |
| thứ tự | `top` → `hero` → `bottom` nối tiếp; các block nối tiếp nhau, **không chồng, không bỏ từ** — trừ đoạn nhường cho `steps` hoặc `hook` |
| độ dài | **1,5–3 s** mỗi block; câu dài tách hai block, vế quá ngắn gộp với vế kề |
| `style` | `script` (mặc định: nghiêng, gradient tím) · `stomp` (chữ đập in hoa màu đặc: luận điểm, con số, câu chốt) · `quote` (stomp kèm ngoặc kép, cho thuật ngữ được trích) |
| `color` | chỉ cho stomp/quote: `warn` (vấn đề, cái sai) · `gold` (giải pháp, con số, CTA) · `ink`; block script để `null` |
| `accent` | index **trong hero** (0 = từ đầu hero) của 1 từ tô cyan: từ chỉ hướng, danh từ chính. Không có thì `null` |
| `display` | `{"<index từ>": "chữ thay thế"}` — chỉ dùng khi phải sửa chữ hiển thị của đúng từ đó; mặc định `{}` |
| `reveal` | `true` cho block script muốn lật mở cả thẻ một lượt (có tiếng đập). Chỉ cho `script` |

Ba luật đếm được:

- **stomp/quote cách nhau ≥ 8 s** (đo giữa hai từ đầu block). Chữ đập liên tiếp
  thì tiếng đập bị gộp và mất hết sức nặng.
- **stomp + quote + reveal ≤ 3 mỗi video.** Đập nhiều là không còn gì để đập.
- Hero của stomp/quote **không được chứa từ khoá CTA** — cuối video sẽ có tiếng
  CTA riêng, để cả hai là đập đôi (đúng lỗi của bản dựng cũ video 02).

## 4. hook — cú mở

- Chỉ đặt hook khi **lời có nói** một con số hoặc một từ đập ở mấy giây đầu
  (`20`, `90%`, `3 LỖI`, `SAI RỒI`). Không bịa chữ không có trong lời.
- `text` ngắn: con số hoặc 1–2 từ, **tối đa 8 ký tự kể cả dấu cách**. Tít tự co
  cho vừa vùng an toàn (`20` giữ cỡ lớn nhất, `SAI RỒI` còn khoảng ba phần tư);
  dài hơn thì chữ nhỏ tới mức mất lực đập.
- `hit_word` = index của từ được nói đó; nó **phải nằm trong hero của một block
  `stomp`** và được nói trong **3,5 s đầu** — hook rơi xuống đúng chữ đập ấy.
- Lời mở không có số hay từ đập → `"hook": null`, đừng cố dựng.
- `color`: `warn` khi hook là vấn đề, `gold` khi là con số hứa hẹn / giải pháp.

## 5. steps — bảng liệt kê

- Chỉ dùng khi lời liệt kê **3–5 mục liền nhau**.
- `range` = các từ của từng mục (bảng lấy mốc hiện theo từ đầu mục),
  `label` = viết gọn ≤ 26 ký tự, `title` = tên bảng in hoa.
- Các `range` nối liền nhau: mục sau bắt đầu đúng từ mục trước hết.
- Các từ trong `range` của steps **không** thuộc block nào (bảng thay phụ đề ở
  đoạn đó); các từ trước và sau bảng vẫn phải có block. Trong khoảng thời gian
  của bảng **không đặt block**.

## 6. shots — cỡ cảnh (camera 2.5D trên một cú quay)

- `cut_at_word` = từ mà máy cắt vào (thời điểm cắt = `on` của từ đó).
  `s0 → s1` = scale đầu → cuối shot (máy trôi chậm 3–6%).
  `x`, `y` = dịch khung theo tỉ lệ khung hình, tự bị chặn trong phần dư khi phóng.
- **Cắt cách nhau 2–4 s**, và **phải cắt vào một khoảng ngắt** (`on` của từ cắt
  cách một khoảng ngắt trong `pauses.json` ≤ 0,6 s) — cắt giữa hơi thở thấy rõ
  là lỗi. Shot đầu (từ 0) là khung mở, không cần snap.
- Luật 2–4 s tính cả **hai mép video**: shot đầu chạy từ 0 s nên cú cắt thật đầu
  tiên phải rơi vào giây 2–4; từ cú cắt cuối tới hết video (khoảng ngắt sau từ
  cuối + 0,5 s) không quá 4 s — trừ khi shot cuối là shot đẩy vào CTA (cắt ở
  hoặc sau từ đầu câu CTA). Một shot tĩnh cả video là lỗi `SHOT_GAP`.
- Xen **toàn** (1,00–1,06) với **cận** (1,14–1,22); **scale ≤ 1,22**, được vượt
  lên tối đa 1,25 cho **nhiều nhất 2 shot** cả video.
- Từ chỉ hướng (trái/phải, bên này/bên kia) → `x: ±0.045` theo hướng đó.
- Lúc bảng `steps` hiện → `y: -0.06` và scale ~1,22 để đẩy mặt lên nhường chỗ
  cho bảng; giữ `y` đó tới hết bảng.
- **Shot cuối đẩy chậm vào CTA**: cắt ở từ đầu câu CTA, `s0 1.06 → s1 1.20`.
- Cú cắt đổi scale ≥ 0,12 sẽ tự có tiếng gió (planner lo, đừng đặt tay).

## 7. cta

- Chỉ ghi khi **lời có nói** CTA. `range` = câu CTA (từ đầu câu tới hết lời),
  `label` = chữ trên viên CTA, `keyword` = cụm từ khoá người xem phải gõ.
- `label` **≤ 14 ký tự**, `keyword` **≤ 16 ký tự** (kể cả dấu cách) — viên CTA
  phải vừa vùng an toàn; dài hơn là lỗi `CTA_TEXT`.
- Lời không nói CTA → `"cta": null`. **Không bịa lời hứa, quà tặng, con số.**
  Nếu user muốn có CTA mà lời không nói, báo user là chữ tự điền rồi mới thêm.

## 8. Bảng mã lỗi của `validate_edit`

| Mã | Nghĩa | Cách sửa |
|---|---|---|
| `SCHEMA` | sai khuôn file, thiếu khoá, index vượt số từ, hoặc bảng `steps` không phải 3–5 mục | so lại với khung `propose_edit.json` |
| `BLOCK_LEN` | block ngoài 1,5–3 s | tách block dài, gộp block ngắn với vế kề |
| `HERO_WORDS` | hero không phải 2–5 từ | đẩy bớt từ xuống `top`/`bottom` |
| `OVERLAP_OR_GAP` | có từ bị bỏ, bị đếm hai lần, hoặc block sai thứ tự | rà lại các range nối tiếp từ 0 tới hết |
| `STEPS` | các mục bảng không liền nhau, hoặc có block bắt đầu trong khoảng bảng | nối liền range các mục; chuyển block đó thành một mục, hoặc dời nó ra ngoài bảng |
| `STOMP_SPACING` | hai nhãn đập cách nhau < 8 s | đổi một cái sang `script` |
| `STOMP_LIKE_MAX` | quá 3 nhãn đập (stomp + quote + reveal) | giữ lại 3 câu đáng đập nhất |
| `REVEAL_STYLE` | `reveal` đặt trên block không phải `script` | tắt `reveal` hoặc đổi style |
| `HIT_WORD` | `hit_word` không nằm trong hero stomp, hoặc nói sau 3,5 s | đưa từ đó vào hero một block stomp, hoặc bỏ hook |
| `CTA_RANGE` | có `cta` nhưng thiếu `range` | ghi range câu CTA, hoặc để `cta: null` |
| `CTA_TEXT` | `cta.label` quá 14 ký tự hoặc `cta.keyword` quá 16 ký tự | rút gọn nhãn (vd `Bình luận`); từ khoá giữ đúng lời nói |
| `CTA_KEYWORD_IN_STOMP` | hero stomp/quote chứa từ khoá CTA | đổi block đó sang `script` |
| `SCALE` | scale vượt 1,22 (quá 2 shot) hoặc vượt 1,25 | hạ scale, xen thêm cảnh toàn |
| `SHOT_GAP` | hai cú cắt cách nhau ngoài 2–4 s; cú cắt đầu ngoài giây 2–4; shot cuối giữ quá 4 s tới hết video (không phải shot đẩy vào CTA) | thêm hoặc bớt một cú cắt; cắt shot cuối ở từ đầu câu CTA |
| `CUT_SNAP` | cú cắt không rơi vào khoảng ngắt | dời `cut_at_word` sang từ mở đầu cụm lời gần nhất |

## 9. Không được làm

- Không viết giây, frame, tên file SFX, mức âm lượng vào `edit.json`.
- Không sửa `words.json`, `pauses.json`, `rules.json`, component hay script.
- Không bịa lời: chữ hiển thị lấy từ `words.json`; chỉ dùng `display` khi sửa
  đúng một từ nghe sai, và phải báo lại trong comment của card.
- Không tự unblock card, không chạy `python -c`, không tự viết script mới.
