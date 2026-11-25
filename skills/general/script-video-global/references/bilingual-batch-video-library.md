# Bilingual batch video library

Dùng cho thư viện nhiều video được tổng hợp từ spreadsheet, content bank, campaign brief hoặc script cũ và sẽ bàn giao cho Media/KOL/Editor.

## Pipeline

### 1. Inspect nguồn và lập inventory

- Đọc nguồn trực tiếp, đúng tab/gid/version.
- Inventory concept hiện có theo ID, title, angle, funnel, customer level, CTA và production type.
- Gắn nhãn dữ kiện: `VERIFIED`, `INFERRED`, `ASSUMED`, `HOLD`.

### 2. Gap audit

Tìm khoảng trống theo bốn trục:

1. **Customer maturity:** beginner/manual, transitioning, established, growth/pilot-ready.
2. **Funnel:** TOFU, MOFU, BOFU, retention/community.
3. **Narrative:** pain, education, process transparency, proof, objection, practical preparation.
4. **Production:** brand/AI, UGC/FGC/EGC, live action, screen demo, B-roll.

Chỉ thêm concept nếu nó lấp ít nhất một khoảng trống rõ ràng và không trùng message chính của video cũ.

### 3. Canonical schema

Mỗi video nên có:

```json
{
  "id": "V-01",
  "titleEn": "",
  "titleVi": "",
  "customerLevel": "Level 1 — ...",
  "funnel": "TOFU",
  "creatorType": "UGC|FGC|EGC|Brand",
  "production": "AI|Quay thật",
  "duration": "30s",
  "status": "Sẵn sàng|Duyệt một phần|HOLD",
  "publishState": "PASS|PASS_WITH_FIXES|HOLD",
  "hookAEn": "",
  "hookAVi": "",
  "hookBEn": "",
  "hookBVi": "",
  "ctaEn": "",
  "ctaVi": "",
  "captionEn": "",
  "captionVi": "",
  "hashtags": [],
  "claimNoteVi": "",
  "productStateVi": "",
  "assetsVi": "",
  "productionBriefVi": "",
  "musicSourceVi": "",
  "talentStatusVi": "",
  "aiDisclosureVi": "",
  "privacyVi": "",
  "rightsVi": "",
  "scenes": []
}
```

Mỗi scene có `time`, `shotId`, `dialogueEn`, `dialogueVi`, `overlayEn`, `visualVi`, `cameraVi`, `audioVi`, `editVi`.

## Bilingual separation

### Public English lane

Chỉ chứa:

- English title.
- Hook A/B.
- CTA.
- Caption và hashtag.
- Dialogue EN.
- Overlay EN.

### Vietnamese production lane

Chứa:

- Title/hook/CTA/caption bản Việt.
- Objective, insight và emotion arc.
- Visual, camera, audio, edit direction.
- Asset list và KOL handoff.
- Product truth, claim note và production safeguards.

Không đặt bản dịch tiếng Việt dưới mỗi hook EN. Không để visual/edit tiếng Việt trong scene table EN. Technical identifiers được giữ nguyên.

## Product truth và CTA

Trước khi dùng CTA, kiểm:

- Destination có thật không?
- Form có hoạt động không?
- Demo/trial/offer/pricing đã được owner duyệt chưa?
- Có thu PII không và privacy notice có đủ không?

Nếu chưa đạt gate, dùng CTA an toàn:

- Save this checklist.
- Follow for the next step.
- Comment the question you want answered next.
- Prepare your asset folder.

Không dùng `Request a demo`, `Start free trial`, `Download`, price hoặc guarantee chỉ vì CTA đó có conversion tốt.

## Rights và production safeguards

Cho mỗi video Media/KOL cần biết:

- Ai xuất hiện và talent release nào cần có.
- Location release.
- Music library/track/licence ID.
- AI-generated content disclosure và watermark.
- PII/demo data/blur rule.
- Logo, font, stock, screen capture và customer asset rights.
- Trigger phải reshoot hoặc giữ HOLD.

`Trending audio` không tự động có commercial licence.

## Status mapping

Dùng ba trạng thái canonical:

```text
PASS            → Sẵn sàng
PASS_WITH_FIXES → Duyệt một phần
HOLD            → HOLD
```

Script có thể hoàn chỉnh về nội dung nhưng vẫn HOLD vì talent, location, product state hoặc rights chưa được duyệt.

## Deterministic QA

- ID unique và liên tục theo convention.
- Số video/count/status/customer-level/production cộng đúng tổng.
- 4–6 scenes/video trừ khi format có lý do khác.
- Dialogue mỗi câu ≤15 từ.
- Hook A/B và CTA có đủ EN/VI.
- 5–8 hashtag/video.
- Không có ký tự ngôn ngữ ngoài ý muốn.
- Không có claim hoặc CTA bị Legal/Product giữ HOLD.
- JSON và UI status mapping khớp.
- Markdown handoff không khác canonical JSON.

Khi cập nhật website, thêm verifier kiểm cả language separation trong component, không chỉ sự tồn tại của `EN`/`VI` tabs.
