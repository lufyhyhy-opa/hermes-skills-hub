---
name: harness-engineering-trust-pyramid
description: "Hệ quy chiếu Harness Engineering & Kim Tự Tháp Niềm Tin 4 Tầng (Lauren Tan — SpaceX/xAI GrokBot Playbook: 3.000 PR/tháng, 0.5% Rollback). Áp dụng nguyên tắc 'Lint > AGENTS.md', khóa vật lý lỗi bằng AST/Linter và bắt buộc Runtime Verification (tự chạy test, decode media, render check, screenshot proof) trước khi bàn giao."
version: 1.0.0
author: LinTech Autonomous Council
license: MIT
metadata:
  hermes:
    tags: [harness-engineering, trust-pyramid, deterministic-lint, runtime-verification, zero-babysitting, lauren-tan, xai, anti-slop]
    category: lintech-os
---

# 🛡️ Harness Engineering & Kim Tự Tháp Niềm Tin 4 Tầng (`harness-engineering-trust-pyramid`)

> **Triết lý cốt lõi (Lauren Tan `@poteto` — Principal Engineer tại SpaceXSI / GrokBot, cựu kỹ sư Cursor & Meta React Core — Hội nghị AI Engineer Code Summit: *"All Code Is Slop, Except Mine"*):**
> - **Số liệu thực chiến:** 1 kỹ sư merge **3.000 PR/tháng** (~100 PR/ngày), toàn đội merge **11.000 PR/tháng** lên production với **tỷ lệ rollback chỉ ~0,5%**.
> - **Phân bổ Token (Quy tắc 30/70):** Chỉ tốn ~30% ngân sách token cho việc sinh code ban đầu; **~70% ngân sách token hàng ngày được dồn cho khâu Kiểm chứng tự động (Verification)** — tự chạy app, quay video/chụp ảnh màn hình làm bằng chứng, kiểm thử theo thuộc tính (property-based testing) và kiểm chứng hình thức (Formal Verification với TLA+ / Lean).
> - **Cảnh báo gốc rễ:** Nếu bạn tự động hóa một vòng lặp lập trình bừa bộn, bạn không xây dựng "nhà máy phần mềm" mà chỉ đang tăng tốc sản xuất **rác AI (AI Slop)**. Hãy cải tạo môi trường thành nơi **con đường ngắn nhất chính là con đường đúng đắn nhất (Pit of Success)**: viết ràng buộc vào trong code (Linter / AST / Runtime Verifier), đừng viết lời khuyên trong tài liệu (`AGENTS.md`).

---

## 1. 4 Quy Luật Sắt Của Harness Engineering

### Quy Luật 1: Bản thân Codebase mới là Prompt lớn nhất (Broken Windows Prevention)
- AI Agent cực kỳ giỏi sao chép mẫu có sẵn trong codebase ("nhìn mèo vẽ hổ" / in-context pattern matching).
- Nếu codebase chứa 1 đoạn code dùng `useEffect` sai cách, dùng `any`, import chéo tầng hoặc chứa comment rác cắt cụt (`// ... rest of code`), Agent sẽ nhân bản lỗi đó ra toàn dự án.
- **Hành động bắt buộc:**
  - Khóa vật lý các API phức tạp dễ bị LLM lạm dụng ở cấp độ kiến trúc/biên dịch (ví dụ: cấm hoàn toàn `useEffect` trong code sản phẩm, chỉ cho phép gọi qua các framework primitives nội bộ đã được kiểm soát chặt).
  - **Cấm ~99% comment trong code (Chặn "Cửa thoát hiểm" của AI):** AI Agent thường dùng comment như một **"lối thoát hiểm" (escape hatch)** để biện minh cho các đoạn code vá víu, hacky hoặc chưa hoàn chỉnh (ví dụ: viết comment giải thích tại sao đoạn hack này "tạm chấp nhận được"). Ngoài ra, comment cũ lệch với code sẽ đầu độc ngữ cảnh của Agent ở các vòng sau. Vì vậy, cấm tuyệt đối comment cắt cụt (`// ... rest of code`), placeholder (`TODO`, `FIXME`) và comment giải thích *What*.

### Quy Luật 2: Mỗi khi Agent phạm lỗi, biến nó thành Rule Lint chứ đừng sửa `AGENTS.md` (`Lint > Prose`)
- Quy tắc viết bằng ngôn ngữ tự nhiên (prose) trong `AGENTS.md` / `CLAUDE.md` mang tính **xác suất** — khi ngữ cảnh dài lên, LLM sẽ quên hoặc phớt lờ.
- Quy tắc kiểm tra tĩnh (ESLint, TypeScript compiler, Python AST Linter) mang tính **tất định 100% (Deterministic)**.
- **Tiêu chuẩn thiết kế thông báo lỗi Linter dành cho AI (`AI-Directed Diagnostics`):**
  - Mọi custom lint rule khi báo lỗi **BẮT BUỘC** chứa chỉ dẫn sửa lỗi trực tiếp trong message:
    `[AI-HARNESS-CONSTRAINT] <Hành vi bị cấm> -> <Cách sửa chuẩn / API thay thế cần dùng ngay>.`
  - Nhờ đó, đầu ra `stderr` của Linter tự động trở thành Prompt sửa lỗi chính xác 100% cho Agent ngay trong vòng lặp thực thi.

### Quy Luật 3: Dùng Kiểm Chứng Thời Gian Chạy (Runtime Verification) để Agent "Tự Chứng Minh Trong Sạch"
- **"Code compile/build thành công" KHÔNG đồng nghĩa với "Tính năng đã chạy đúng".**
- Trước khi báo cáo hoàn thành bất kỳ tác vụ code, web UI, slide HTML hay media pipeline nào, Agent bắt buộc phải chạy script kiểm chứng runtime để thu thập **Bằng Chứng Thực Thi (`Proof-of-Work Receipt`)**:
  - **Với Web / Next.js / Landing Page / Slide HTML:** Chạy `lint` + `typecheck` + `verify_harness` (kiểm tra đủ cấu trúc section, design tokens, không còn placeholder, build production thành công hoặc chụp screenshot giao diện thật).
  - **Với Python / Data / Media / Trading Pipeline:** Chạy `lint_architecture.py` (AST check) + `preflight` + unit tests + `verify_outputs.py` (giải mã thật file video/audio bằng FFmpeg/PyAV, kiểm tra schema JSON/CSV, xác nhận không có template `{{...}}` chưa render).

### Quy Luật 4: Xây Dựng "Kim Tự Tháp Niềm Tin" Từ Dưới Lên (The 4-Layer Pyramid of Trust)

```text
            /\
           /  \        Tầng 4: Con Người Duyệt (Anh Huy — Chiến lược, Thẩm mỹ & Quyết định cuối)
          /----\
         /      \      Tầng 3: Kiểm Chứng Runtime (Tests, Media Decode, Render Proof, Screenshot, Receipt JSON)
        /--------\
       /          \    Tầng 2: Phân Tích Tĩnh Tất Định (ESLint, TypeScript Strict, Python AST Architecture Linter)
      /------------\
     /              \  Tầng 1: Ràng Buộc Codebase Vật Lý (Module Boundaries, Ban Dangerous APIs, Zero Truncation)
    /________________\
```

- **Tuyệt đối không đẩy rác lên Tầng 4:** Nếu Tầng 1, Tầng 2 hoặc Tầng 3 thất bại (`exit code != 0`), Agent phải tự sửa ngay trong vòng lặp nội bộ cho đến khi cả 3 tầng dưới đều `PASSED`, xuất ra file `trust_pyramid_receipt.json` / `harness_verification_receipt.json` rồi mới được phép trình lên Anh Huy.

---

## 2. Quy Trình Thực Thi Chuẩn & Công Cụ CLI Toàn Cục (`hermes-verify-harness`)

Mọi Agent trong hệ thống Hermes (`agent-00` → `agent-18` và `ai-trading`) đã được trang bị công cụ kiểm chứng tất định toàn cục tại `/Users/buithiphuongthao/.local/bin/hermes-verify-harness` (và `~/.hermes/bin/hermes-verify-harness`):

1. **Bước 1 — Kích hoạt Ràng buộc Tầng 1, Tầng 2 & Tầng 3 bằng CLI Toàn Cục:**
   - Kiểm chứng bất kỳ file thành phẩm nào (`.html`, `.pptx`, `.md`, `.py`, `.json`, `.tsx`) hoặc toàn bộ thư mục dự án:
     ```bash
     /Users/buithiphuongthao/.local/bin/hermes-verify-harness <đường_dẫn_file_hoặc_repo> --receipt <đường_dẫn>/trust_pyramid_receipt.json
     ```
   - Trong dự án Next.js / TypeScript (`ai-website-cloner-template`):
     ```bash
     npm run verify
     ```
   - Trong dự án Python (`MoneyPrinterV2`):
     ```bash
     ./run_autonomous.sh --verify
     ```
2. **Bước 2 — Vòng lặp Tự Chữa Lành Tất Định (Deterministic Self-Healing Loop — 70% Verification Effort):**
   - Nếu `hermes-verify-harness` hoặc Linter báo lỗi `[AI-HARNESS-CONSTRAINT]`, đọc thẳng chỉ dẫn `[AI-FIX-DIRECTIVE]` trong thông báo lỗi, sửa triệt để tại mã nguồn/bản thảo và chạy lại cho đến khi `"status": "PASSED"` (`violation_count: 0`).
3. **Bước 3 — Đóng băng bài học mới thành Rule Lint (Continuous Rule Codification — `Lint > AGENTS.md`):**
   - Mỗi khi phát hiện một lỗi lặp lại của Agent (ví dụ: quên màu thương hiệu Area `#485C11`, dùng `useEffect` gây lỗi hydration, để sót `{{variable}}` trong HTML, dùng comment cắt cụt `// ... rest of code`, hay dùng văn mẫu AI Slop), hãy **bổ sung ngay rule kiểm tra tĩnh vào `hermes-verify-harness` / `verify_harness.mjs` / `lint_architecture.py` / `eslint.config.mjs`** để lỗi đó vĩnh viễn không bao giờ tái diễn.
