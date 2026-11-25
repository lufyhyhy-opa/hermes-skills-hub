---
name: comfyui-family-filmmaker
description: Sản xuất phim ngắn gia đình 3 nhân vật người thật (Ba, Mẹ, Con gái) theo công thức triệu view của kênh "Linh Mít Daily" (9:16 Reels/TikTok 15-18s) bằng Quy trình 3 bước trên ComfyUI: (Bước 0) Dùng skill ai-video-prompt & rea-video bóc tách từng phân cảnh từ video mẫu -> (Bước 1) Khóa mặt 3 nhân vật & khóa bố cục Frame Đầu/Cuối từng phân cảnh -> (Bước 2) Duyệt ảnh khóa mặt rồi mới xuất Clip First-Last-Frame.
---

# ComfyUI 3-Step Scene-Locked & Face-Locked Family Filmmaker (`comfyui-family-filmmaker`)

## 1. Kiến Trúc Quy Trình 3 Bước (Tích Hợp `ai-video-prompt` & `rea-video`)

### BƯỚC 0 — Bóc Tách Từng Phân Cảnh Từ Video Mẫu (`ai-video-prompt` + `rea-video`)
Khi có một video mẫu (ví dụ: một Reel triệu view của kênh **Linh Mít Daily**), hệ thống tự động gọi skill `ai-video-prompt` (`/Users/buithiphuongthao/.hermes/shared-skills/video/ai-video-prompt/scripts/probe_video.py` & `reverse.py`) và `rea-video` để:
1. **Bắt chính xác điểm chuyển cảnh (`FFmpeg Scene Detection`)**: Chia video thành từng phân cảnh độc lập (`Shot S01`, `Shot S02`, ...).
2. **Trích xuất Cặp Ảnh Khung Xương Đầu – Cuối (`shot_S01_first.jpg` & `shot_S01_last.jpg`)**: Lấy frame đầu tiên và frame kết thúc của từng phân cảnh để làm **Ảnh Tham Chiếu Khóa Bố Cục (`image 4`)**.
3. **Phân tích Góc máy, Hành động & Biểu cảm (`structured.json`)**: Tự động dịch ngược góc máy, bối cảnh, hành động và ánh xạ nhân vật trong video gốc sang **3 nhân vật gia đình cố định**:
   - Nhân vật Bố/Nam trong video mẫu $\rightarrow$ **`image 1` (Ba / Anh Huy)**
   - Nhân vật Mẹ/Nữ trong video mẫu $\rightarrow$ **`image 2` (Mẹ / Vợ)**
   - Nhân vật Bé gái/Con nhỏ trong video mẫu $\rightarrow$ **`image 3` (Con gái - "Bình rượu mơ")**

### BƯỚC 1 — Cổng Khóa Mặt Nhân Vật & Khóa Phân Cảnh Trước Khi Ra Clip (`Scene & Face Lock Gate`)
Trong file workflow `/Users/buithiphuongthao/Desktop/veo/linh_mit_3buoc_khoa_mat_va_phan_canh_9x16.json`:
- **Node `BƯỚC 1A (First Frame Lock)` & `BƯỚC 1B (Last Frame Lock)` (`Flux3ImageNode` / `PuLID-Flux` + `ReActor`):**
  - Nhận đồng thời **4 đầu vào ảnh**:
    - `image 1`: Ảnh chân dung **Ba**
    - `image 2`: Ảnh chân dung **Mẹ**
    - `image 3`: Ảnh chân dung **Con gái**
    - `image 4`: **Ảnh Frame Đầu (`BƯỚC 0A`) / Frame Cuối (`BƯỚC 0B`)** bóc tách từ phân cảnh video gốc.
  - Sinh ra cặp ảnh **`Shot_First_Frame_Locked`** và **`Shot_Last_Frame_Locked`** giữ nguyên 100% bố cục, góc máy, ánh sáng và tư thế diễn xuất của phân cảnh gốc nhưng mang **khuôn mặt thật của Ba, Mẹ và Con gái**.
- **Cơ chế Khóa Chặn Trước Khi Ra Clip (`--lock-before-video` mặc định BẬT):**
  - Node tạo video ở Bước 2 mặc định được đặt ở chế độ **Bypass (`mode: 4`)** để bạn và Agent kiểm tra, duyệt 2 bức ảnh khóa mặt Đầu – Cuối của từng phân cảnh trước khi tiêu tốn tài nguyên render video.

### BƯỚC 2 — Xuất Video Khóa Đầu – Cuối Không Trôi Mặt (`Veo 3.1 First-Last-Frame to Video`)
- Sau khi 2 bức ảnh `Shot_First_Frame_Locked` và `Shot_Last_Frame_Locked` đã khóa chuẩn mặt 3 người và đúng bố cục phân cảnh, bật Node **BƯỚC 2 (`Veo3FirstLastFrameNode`)** (`Cmd + B` trên ComfyUI hoặc truyền cờ `--enable-video-step` trong CLI).
- Node `Veo3FirstLastFrameNode` nhận cả **`first_frame`** lẫn **`last_frame`** đã khóa mặt cùng kịch bản chuyển động từ `ai-video-prompt`, giúp video đầu ra **không bao giờ bị biến dạng mặt ở cuối cảnh hay đi lệch kịch bản gốc**.

---

## 2. Lệnh CLI Tự Động Hóa Cho Hermes (`agent-09-scriptwriter` & `agent-10-video-editor`)

### Chế độ A: Bóc tách từ Video Mẫu + Khóa Mặt & Phân Cảnh (Khuyên dùng)
```bash
/Users/buithiphuongthao/.local/bin/comfyui-family-film \
  --ref-video "/path/to/linh_mit_sample.mp4" \
  --dad "/path/to/anh_ba.jpg" \
  --mom "/path/to/anh_me.jpg" \
  --daughter "/path/to/anh_con_gai.jpg" \
  --aspect 9:16
```
Lệnh trên sẽ:
1. Chạy `ai-video-prompt` (`probe_video.py` + `reverse.py`) bóc tách toàn bộ các phân cảnh `S01`, `S02`... vào `/Users/buithiphuongthao/Desktop/veo/scene_breakdown/`.
2. Tự động cắt `first_frame` và `last_frame` của từng phân cảnh nạp vào `ComfyUI/input/`.
3. Xuất ra các file workflow đã khóa sẵn từng phân cảnh: `ComfyUI/user/default/workflows/locked_scene_S01.json`, `locked_scene_S02.json`... (với Bước 2 tạo Video đang tạm khóa `Bypass` để duyệt mặt trước).

### Chế độ B: Chạy kịch bản mới không cần video mẫu
```bash
/Users/buithiphuongthao/.local/bin/comfyui-family-film \
  --dad "/path/to/anh_ba.jpg" \
  --mom "/path/to/anh_me.jpg" \
  --daughter "/path/to/anh_con_gai.jpg" \
  --aspect 9:16 \
  --shot1-img-prompt "Vertical 9:16 photorealistic candid home video frame..." \
  --shot1-vid-prompt "Static tripod home-video shot in 9:16 vertical format..."
```

---

## 3. Đường Dẫn Các File Workflow & Tài Liệu Trong `/Users/buithiphuongthao/Desktop/veo`
- Workflow 3 bước (Bóc tách phân cảnh $\rightarrow$ Khóa mặt First/Last Frame $\rightarrow$ Xuất Clip): `/Users/buithiphuongthao/Desktop/veo/linh_mit_3buoc_khoa_mat_va_phan_canh_9x16.json`
- Workflow 2 cảnh liên hoàn 9:16: `/Users/buithiphuongthao/Desktop/veo/linh_mit_style_gia_dinh_9x16.json`
- Báo cáo phân tích kênh Linh Mít Daily & 5 kịch bản mẫu: `/Users/buithiphuongthao/Desktop/veo/KE_HOACH_KENH_GIA_DINH_LINH_MIT_STYLE.md`
