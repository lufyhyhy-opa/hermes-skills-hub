---
name: ai-video-prompt
description: "Reverse-engineer any reference video into scene-by-scene (shot-by-shot) generation prompts, character/avatar look specs, camera movements, and evidence frames for HeyGen, Seedance, Veo, Sora, Kling, and Wan. Use when the user says video-to-prompt, dịch ngược video ra prompt, lấy prompt từng phân cảnh từ video, tách cảnh video làm HeyGen, or 视频反推提示词."
version: 1.1.0
author: wonfull888 (integrated & enhanced for Hermes Agent)
license: Custom (Non-Commercial)
platforms: [linux, macos, windows]
metadata:
  tags: [video, video-to-prompt, reverse-engineer, scene-breakdown, heygen, veo, sora, kling, seedance, ffmpeg]
  hermes:
    tags: [VideoToPrompt, ReverseEngineerVideo, SceneBreakdown, HeyGenPrompt, Video, Media]
    related_skills: [openmontage, ai-video-editor, dung-video-talking-head, video-short]
---

# AI Video Prompt (`wonfull888/ai-video-prompt` — BestPrompts Pipeline for Hermes)

Installed at:
- Shared Skill Root: `/Users/buithiphuongthao/.hermes/shared-skills/video/ai-video-prompt`
- Workspace Mirror: `/Users/buithiphuongthao/Desktop/reseach/ai-video-prompt`

## Khi nào sử dụng (When to Use)
Kích hoạt skill này ngay khi người dùng yêu cầu:
- `video-to-prompt <đường_dẫn_video>` hoặc `ai-video-prompt <đường_dẫn_video>`
- "Dịch ngược video này ra prompt từng phân cảnh"
- "Bóc tách kịch bản / phân cảnh (shot-by-shot) từ video mẫu để làm video tương tự trên HeyGen / Veo / Sora / Kling / Seedance"
- `视频反推提示词 <视频路径>`

## Cách chạy (Quick Execution)

Hệ thống đã được cấu hình tự động nhận diện `ffmpeg`/`ffprobe` tại `/Users/buithiphuongthao/.local/bin` và tự động nạp API Key từ `~/.hermes/.env` (`HERMES_CUSTOM_VILAO_API_KEY` với model `gpt-6.1-sol` có hỗ trợ Vision, hoặc `OPENROUTER_API_KEY` / `DEEPSEEK_API_KEY` nếu có).

### Chế độ 1: Chạy nhanh (Fast Single-Pass — Khuyên dùng, ~15–25 giây)
Trích xuất các frame đại diện theo phân cảnh, phân tích toàn bộ nhân vật (Avatar Look), góc máy, hành động từng Shot và xuất ra bộ Prompt đầy đủ:

```bash
python3 /Users/buithiphuongthao/.hermes/shared-skills/video/ai-video-prompt/scripts/reverse.py "<đường_dẫn_video>" --out "<thư_mục_output>" --frames 12
```

### Chế độ 2: Chạy chuyên sâu đa tầng (Full Multi-Pass PRO Pipeline)
Tự động bắt điểm cắt cảnh (`ffmpeg scene detection`), kiểm tra chuyển động dày đặc (`motion_review`), kiểm tra biểu cảm khuôn mặt (`expression_review`), đối soát nhân quả (`reconcile`) và xuất bộ hồ sơ đầy đủ:

```bash
python3 /Users/buithiphuongthao/.hermes/shared-skills/video/ai-video-prompt/scripts/reverse_full.py "<đường_dẫn_video>" --out "<thư_mục_output>"
```

### Chế độ 3: Chỉ trích xuất Frame phân cảnh & Metadata bằng FFmpeg (Offline 100%)
Nếu chỉ cần cắt cảnh tự động bằng FFmpeg + trích xuất ảnh chụp từng phân cảnh + tách file âm thanh WAV 16kHz để Agent tự xem trực tiếp:

```bash
python3 /Users/buithiphuongthao/.hermes/shared-skills/video/ai-video-prompt/scripts/probe_video.py "<đường_dẫn_video>" --output-dir "<thư_mục_output>" --extract-audio --overwrite
```

## Các file kết quả đầu ra (Deliverables)
Sau khi chạy lệnh ở Chế độ 1 hoặc Chế độ 2, trong `<thư_mục_output>` sẽ có sẵn:
1. **`heygen_scenes.md`**: Bảng phân cảnh chi tiết từng Scene (`Shot S01`, `Shot S02`...) thiết kế riêng cho **HeyGen & AI Video**:
   - **Phần 1 (Avatar Look & Character Setup)**: Ngoại hình, trang phục, đạo cụ, ánh sáng, môi trường để tạo Avatar trên HeyGen.
   - **Phần 2 (Prompt Từng Phân Cảnh)**: Thời lượng từng cảnh, góc máy, hành động/biểu cảm và khối code Prompt copy-paste cho từng Scene.
2. **`prompt.md`** (`prompt_en.md` / `prompt_zh.md` / `prompt_en.txt`): Prompt tổng thể + từng Shot (Positive & Negative Prompts).
3. **`shots.md`**: Bảng tổng hợp các phân cảnh theo mốc thời gian.
4. **`evidence_gallery.md`**: Bộ sưu tập ảnh chụp (Keyframes) thực tế của từng phân cảnh.
5. **`structured.json`**: Dữ liệu JSON chuẩn hóa toàn bộ phân cảnh, nhân vật, góc máy, chuyển động.

## Quy tắc trả kết quả cho người dùng (Output Rules)
Khi chạy xong pipeline:
1. Đọc file `heygen_scenes.md` và `evidence_gallery.md` trong thư mục kết quả.
2. Trình bày rõ ràng cho người dùng:
   - **Prompt tạo Nhân vật / Avatar (Global / Avatar Look)**
   - **Danh sách Prompt từng phân cảnh (`Shot S01`, `Shot S02`, ...)** kèm mốc thời gian, góc máy, hành động và ảnh chụp phân cảnh đó.
3. Không tự bịa đặt lời thoại, thương hiệu hoặc hiệu ứng không có trong video gốc.

## Tài liệu tham chiếu (References)
- `/Users/buithiphuongthao/.hermes/shared-skills/video/ai-video-prompt/references/analysis-contract.md`: Chuẩn cấu trúc JSON phân tích phân cảnh.
- `/Users/buithiphuongthao/.hermes/shared-skills/video/ai-video-prompt/references/model-adapters.md`: Hướng dẫn tối ưu prompt cho từng nền tảng (Veo, Sora, Kling, Wan, Seedance, Generic).
