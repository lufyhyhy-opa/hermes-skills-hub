# edit.json — file duy nhất agent viết

Mọi số `[a, b)` là **index trong `scripts/words.json`** (bảng do `transcribe.py`
in ra), nửa mở: `[4, 6)` = từ 4 và 5. Thời gian tự lấy từ mốc của từng từ.

```jsonc
{
  "source": "D:/.../1.mp4",               // new_project.py điền sẵn
  "fix":   { "118": "Ánh sáng" },         // index → chữ hiển thị (sửa lỗi ASR)
  "hook":  { "text": "90%", "color": "gold" },          // hoặc null
  "blocks": [ { "id": "b01", "top": [2,4], "hero": [4,6], "bottom": [6,12],
                "style": "stomp", "color": "warn", "accent": null } ],
  "steps": { "title": "4 THÔNG TIN …", "items": [ { "range": [72,76], "label": "…" } ] },  // hoặc null
  "shots": [ { "t": 0.0, "s0": 1.15, "s1": 1.21, "x": 0, "y": 0 } ],
  "cta":   { "label": "Bình luận", "keyword": "PROMPT", "start": 42.4 }                    // hoặc null
}
```

## blocks — thẻ phụ đề 3 tầng

Mỗi block là một thẻ: dòng nhỏ trên / **dòng hero** / dòng nhỏ dưới, cùng hiện
trên màn. Ba dòng ghép lại thành một câu hoặc một vế câu.

| Trường | Quy tắc |
|---|---|
| `top`, `bottom` | từ dẫn / từ đuôi, cỡ nhỏ. Không bắt buộc. |
| `hero` | **2–5 từ mang nghĩa** (luận điểm, từ khoá). ≤ ~18 ký tự thì to nhất. |
| thứ tự | các range nối tiếp, không chồng, không bỏ từ — trừ đoạn nhường cho `steps`/`hook` |
| độ dài | 1.5–3s mỗi block. Câu dài thì tách 2 block. |
| `style` | `script` mặc định (nghiêng, gradient tím). `stomp` = chữ đập in hoa màu đặc cho luận điểm, con số, câu chốt — **tối đa 1 lần / 8–10s**. `quote` = stomp kèm ngoặc kép, cho một thuật ngữ được trích. |
| `color` | chỉ cho stomp/quote: `warn` (vấn đề, cái sai), `gold` (giải pháp, con số, CTA), `ink` |
| `accent` | index **trong hero** của 1 từ tô cyan — từ chỉ hướng (trái/phải), danh từ chính |

## fix — sửa lỗi nghe

- Một index → một cụm hiển thị. Lời sai nhiều từ thì sửa **từng index** cho khớp số từ
  (ví dụ 5 từ sai → 5 key), để mốc thời gian vẫn đúng.
- Bỏ dấu câu cuối từ là tự động, không cần fix.

## hook — cú mở

Số hoặc từ đập vào mắt ở giây đầu (`90%`, `3 LỖI`, `SAI RỒI`). Block đầu tiên
**không được** chứa các index hook đã đọc — nếu không chữ hiện hai lần.

## steps — bảng liệt kê

Chỉ khi lời liệt kê 3–5 mục liền nhau. `range` = các từ của mục (lấy thời điểm
bắt đầu), `label` = viết gọn lại ≤ 26 ký tự. Trong khoảng thời gian của bảng
**không đặt block**.

## shots — cỡ cảnh (camera 2.5D trên một cú quay)

`t` = thời điểm cắt (giây). `s0 → s1` = scale đầu → cuối shot (máy trôi chậm).
`x`, `y` = dịch khung theo tỉ lệ khung hình, tự bị chặn trong phần dư khi phóng.

- Cắt ở ranh giới câu/block, cách nhau **2–4s**.
- Xen **toàn** (1.00–1.06) với **cận** (1.14–1.22); trong shot trôi 3–6%.
- Từ chỉ hướng → `x: ±0.045` theo hướng đó.
- Lúc bảng `steps` hiện → `y: -0.06`, scale ~1.22 để đẩy mặt lên nhường chỗ.
- Shot cuối: đẩy chậm vào CTA (`s0 1.06 → s1 1.20`).
- Cú cắt đổi scale ≥ 0.12 tự có whoosh (nếu không trùng SFX khác).

## cta

Chỉ ghi khi **lời có nói** CTA. Lời không nói → vẫn có thể để placeholder nhưng
phải báo user là tự điền. Không bịa lời hứa, quà tặng, con số.
