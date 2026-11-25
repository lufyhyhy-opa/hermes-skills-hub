# Changelog

Định dạng tự do (không theo Keep a Changelog), mốc theo `metadata.version` của `SKILL.md`.

## [1.1.0] — 2026-09-12

Tái cấu trúc lớn: rules-as-data (`rules.json` + `rules.schema.json`), planner
SFX/BGM tất định theo khoảng ngắt (S01–S29), một trục âm thanh duy nhất (stem +
mux ffmpeg), ánh xạ video↔kịch bản theo nội dung (không dán tay), stage PREP,
pipeline 4 card/video trên Hermes kanban, và `verify.py` (V1–V7) tất định.

**Ngoại lệ khoá version (spec §4.3):** 1.0.0 → 1.1.0 là lần **duy nhất** một
bản minor được phép đổi cả schema (`edit.json` 1.0 → `edit/1.1`, chỉ số từ thay
vì giây) và thứ tự pipeline trong một lần. Từ bản này trở đi: patch = đổi số
luật hoặc sửa lint; minor = thêm luật/stage; major = đổi schema hoặc thứ tự
pipeline.

### Phán quyết đáng chú ý

- **R9** — khâu đỉnh giọng (`thlib/voice.py`): chain gain tuyến tính → `alimiter`
  (ngưỡng = trần TP đích − 0,5 dB, `level=false`, `latency=true`) → loudnorm
  tuyến tính hai lượt; `vo_clear` raise khi ffmpeg báo lượt phi tuyến. Lý do:
  giọng HeyGen có PLR 13,9–16,3 dB nên đạt −16 LUFS với TP ≤ −2 dBTP không thể
  chỉ bằng gain tuyến tính; limiter look-ahead là thực hành R128 chuẩn, đo tốn
  ≤ 0,08 LU và giữ xcorr ở −0,08 ms.
- **R19 / R35** — khâu đỉnh cho final/nobgm/social (`thlib/mix.py`): R19 áp lại
  đúng pattern R9 cho mix cuối; R35 tinh chỉnh riêng cho **file social giao
  cho user**: loudnorm tuyến tính hai lượt trên `mix.wav` (lossless, chưa
  encode) qua limiter true-peak (ngưỡng = trần đích − 0,5 dB) rồi mới encode
  AAC, đo lại TP như L11 và hạ trần thêm đúng phần vượt + 0,1 dB, tối đa 3 lần
  thử — vì bộ limiter theo mẫu của R19 áp trực tiếp lên AAC fail TP sau khi
  encode lần hai (cộng thêm 0,09–3,2 dB không đoán trước được) trên 6/6 project
  thật; cách của R35 đạt 6/6, 5/6 ngay lần thử đầu ở −2,0 dBTP.
- **R26 / R29** — probe text-safe (`check_text_safe.py`, `Subtitle.tsx`): R26
  giữ nguyên nghĩa đen "alpha > 0 ngoài hộp là FAIL" của B14, nhưng probe render
  `TextOnly` **tắt trang trí** (glow, drop/text/box-shadow, backdrop-blur) —
  chỉ đo glyph và nền/viền thẻ, pill; R29 giữ nguyên bốn loại tắt của R26
  nhưng vẫn đo blur/opacity chuyển động, và thêm quy tắc
  `steps.out = min(item cuối.e + 0,15; block sau.show đầu tiên − 0,10)` để thẻ
  liệt kê tắt trước khi block sau hiện. Lý do: đo `alpha > 0` trên hiệu ứng mềm
  từng ép layout che miệng người nói ở Task 11; ý B14 là chữ không đè lên UI
  nền tảng, không phải cấm mọi hiệu ứng mềm.
- **R30 / R31** — từ cuối mỗi block đọc được (`thlib/picture.py`,
  `Subtitle.tsx`): R30 bắt từ cuối mỗi block đậm ≥ 90 % trong ≥ 3 frame liền
  trước khi tắt, dùng chuyển nhanh 2 khung khi thoát thường 6 khung sẽ cắt mất
  nó; R31, khi vẫn không đủ, dời mốc hiện (`display_shift_s`) ≤ 0,15 s mỗi từ
  (từ bị lùi ≤ 0,10 s sau onset thật, sự kiện đã đồng bộ không bao giờ dời) —
  còn lại thì gắn cảnh báo `LAST_WORD_TIGHT` (CONCERN, không FAIL). Lý do:
  7/17 block của video 02 cắt mất từ cuối ở bản 1.0.0 — một lỗi phụ đề thấy
  được; sau R30–R31 cả 17/17 block đọc được.

### Thêm

- `thlib` (pure functions, unit test riêng) + CLI mỏng trên `stage.py`:
  P0 (`intake.py`, `make_cards.py`) → PREP → APPROVE-PREP → INTAKE → PLAN →
  BUILD → VERIFY → APPROVE-CANARY (spec §9, §10).
- `rules.json` + `rules.schema.json`: mọi số nằm trong dữ liệu, khoá qua
  `rules.lock` + `releases/1.1.0/MANIFEST.sha256` (spec §4.3).
- `verify.py` (V1–V7) tất định; `check_prep.py`, `check_text_safe.py`.
- `releases/1.1.0/stages/OPERATOR.md` cho opa-operator (Ruling R15); `collect_kpi.py`
  gom `out/verify/kpi.json` vào `_batches/<b>/kpi.jsonl`, in danh sách video gửi user
  duyệt (D5) và xoá `node_modules` khi đóng lô.
- `tools/check_drift.py` (M0, chỉ đọc; 9 mục, gồm con trỏ SOUL.md của operator/
  editor/verifier và board `vm-heygen-1` + card `t_81a309b2` đã archive — spec
  §13.1 mục 2 và 4 — và thư mục skill đang dùng sạch theo git) và `tools/make_manifest.py` — công cụ dev, để ở `tools/` vì
  Hermes không liệt kê thư mục này cho worker.

### Đổi

- Schema `edit.json`: 1.0 (giây) → `edit/1.1` (index từ trong `words.json`).
- Trục âm thanh: một stem duy nhất render bằng Python + mux ffmpeg, thay chuỗi
  ghép tay nhiều lớp của 1.0.0.
- `SKILL.md`: từ quy trình đầy đủ (agent tự viết `edit.json`, tự build/render)
  thành router ≤ 40 dòng trỏ vào `stage.py` + `stages/PREP.md` / `PLAN.md` —
  bản 1.0.0 vẫn xem được qua `git show v1.0.0:SKILL.md`.
- **R36** — bố cục gốc skill: `references/`, `scripts/` (`new_project.py`),
  `assets/` (pack SFX 1.0.0), `template/`, `examples/` của 1.0.0 chuyển vào
  `legacy/1.0.0/` (giữ nguyên cấu trúc bên trong, `new_project.py` vẫn chạy tại
  chỗ). Lý do: Hermes đưa `references/`, `templates/`, `assets/`, `scripts/` ở
  gốc skill vào prompt của mọi worker như "supporting files" — tài liệu 1.0.0
  (schema tính bằng giây) ở đó mở lại kênh trôi "chép từ bản trước" (spec §4.3).
  Tag `v1.0.0` giữ bố cục gốc.
