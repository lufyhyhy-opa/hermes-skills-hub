# Thông số phong cách — đã chỉnh trên footage thật

Chỉ đổi khi user yêu cầu. Mỗi mục ghi file chứa nó.

## Khung hình

- Xuất 1080×1920, 30fps, h264 crf 18. Nguồn 25fps vẫn dùng được, Remotion lấy frame gần nhất.
- Master 1620×2880: phóng tới 1.5× vẫn nét. (`new_project.py`)

## Chữ (`src/theme.ts`, `src/comp/Subtitle.tsx`)

| Vai | Font | Cỡ (px @1080) |
|---|---|---|
| Hero `script` | Be Vietnam Pro Black Italic (`HERO_SCRIPT_FONT`) | 150 → co theo độ dài, tối thiểu 88 |
| Hero `stomp`/`quote` | DT Phudu Black, in hoa | 176 → tối thiểu 98 |
| Dòng nhỏ trên/dưới | Be Vietnam Pro Medium | 54 → tối thiểu 38 |
| Hook | Bebas Neue Việt hoá | 460 |
| Nhãn bảng, số thứ tự | Bebas Neue; nhãn mục DT Phudu Bold | 34 / 54 / 58 |

- Khối phụ đề neo đáy, cách đáy 400px — nằm trên ngực, dưới cằm.
- Gradient hero: `#fbf9ff → #d7ccff → #b3a4ff`, mỗi từ lấy một lát → đọc ra một dải liền.
  Đầu tối hơn `#b3a4ff` là chìm vào áo đen.
- Hero có quầng sáng tím (bản sao nhoè 22px) + `drop-shadow(0 8px 22px rgba(0,0,0,.8))`.
- Màu đặc: `warn #ff5d73`, `gold #ffcf6b`, accent cyan `#5ec8ff`.
- Merolat (didone nghiêng mảnh) giống video mẫu nhất nhưng mảnh — đổi `HERO_SCRIPT_FONT = FONT.script` nếu user đòi.

## Chuyển động chữ (theo recipe card `blur-slide` của video-shotcraft)

- Mỗi từ hiện sớm 0.05s so với lúc nói (`LEAD`), trong 9 frame, ba kênh cùng một đường `outCubic`:
  `translateY 40→0` (dòng nhỏ 24), `blur 12→0` (dòng nhỏ 8), `opacity 0→1`.
  Ba kênh phải chung một tiến độ — tách ra là thấy "tới rồi mà còn nhoè".
- Block rời đi trong 6 frame: mờ + nhoè 6px + trôi lên 20px, xong trước block sau 0.02s.
- Hook: vào 0.34s (scale 1.34→1, nhoè 26→0), giữ tới 1.08s và đẩy nhẹ 5%,
  rồi thu 42% + rơi xuống chỗ phụ đề trong 0.42s.

## Camera (`src/comp/Footage.tsx`, số liệu trong `edit.json → shots`)

- Cắt cứng đầu shot + 5 frame nảy (+1.8% scale, sáng lên nhẹ) + 3 frame nhoè 5px → đọc ra "cắt máy".
- Trong shot trôi `inOut` từ `s0` đến `s1`; tâm phóng `50% 32%` (mặt).
- Phần dịch `x/y` tự bị chặn trong `(scale − 1) / 2` → không bao giờ lòi mép đen.

## Màu (`src/comp/Grade.tsx`)

`saturate 1.06 contrast 1.06` + vignette elip đen 46% ở mép + scrim đáy 66% + scrim đỉnh 42% + grain 4.5% overlay dịch theo frame.

## SFX (`scripts/build.py`)

Từ vựng cho video người nói: whoosh / impact / pop / sparkle. **Không** dùng tiếng UI
tổng hợp (tone, bleep, notification) — nghe như game.

| Sự kiện | File | Âm lượng thiết kế |
|---|---|---|
| Hook đập xuống | `impact/bass-hit-short` | 0.55 |
| Hero `stomp`/`quote` | `impact/hit-blow` ⇄ `impact/bass-hit-short` | 0.42 |
| Hero `script` | `transition/swoosh-quick` ⇄ `transition/sweep-short` | 0.20 / 0.17 xen kẽ |
| Bảng trượt vào | `transition/swoosh-quick` | 0.26 |
| Từng mục bảng | `ui/pop-electric`, giảm dần 10%/mục | 0.40 |
| CTA | `light/sparkle-touch` | 0.30 |
| Cắt cỡ cảnh ≥ 0.12 | `transition/air-woosh-quick` | 0.14 |

Ba quy tắc cứng, đều đã nằm trong code:

1. **Căn theo đỉnh:** `from = frame đích − độ trễ đỉnh của file − 1.28` (1.28f = độ trễ
   AAC priming của Remotion 4.x / AAC 48kHz / mp4). File có đỉnh muộn tới 14 frame.
2. **Né giọng:** SFX rơi vào lúc đang nói bị hạ để RMS 100ms thấp hơn giọng ≥ 3 dB.
   Khe lặng giữa câu thì giữ âm lượng thiết kế.
3. **Chống "súng máy":** hai mẫu xen kẽ + âm lượng lệch nhẹ; chuỗi liên tiếp thì giảm dần.

Đổi phiên bản Remotion, codec, sample rate hoặc container → chạy `check_av_sync.py`;
lệch đều một lượng thì sửa `OUTPUT_AUDIO_OFFSET_F` đúng lượng đó.

## Không làm (trừ khi user yêu cầu)

- Nhạc nền (BGM): nếu thêm, âm lượng ~0.34, fade 1s đầu / 1.7s cuối, và render thêm một bản không BGM.
- Chữ phía sau người (tách nền): cần matting, template không có.
