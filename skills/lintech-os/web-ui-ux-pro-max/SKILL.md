---
name: web-ui-ux-pro-max
description: "Use when designing and implementing production-grade Web UI/UX, High-Conversion Landing Pages, SaaS Dashboards, Design Systems (DESIGN.md tokens), Bento Grids, and Interactive Prototypes for Agent 17 (Web Designer) and Agent 18 (Brand & Design System Architect)."
version: 2.0.0
author: LinTech Content OS × ui-ux-pro-max-skill × jakubkrehel/skills × claude-design
license: MIT
metadata:
  hermes:
    tags: [web-design, ui-ux, landing-page, design-system, tailwind, shadcn, anti-slop, conversion]
    category: creative
    related_skills: [claude-design, popular-web-designs, brand-guidelines, webapp-testing]
---

# Hệ Thống Thiết Kế Web, UI/UX Chuyển Đổi Cao & Chống AI-Slop (`web-ui-ux-pro-max`)

Skill này tổng hợp tinh hoa từ **`nextlevelbuilder/ui-ux-pro-max-skill`**, **`jakubkrehel/skills`** (`better-interface`, `better-typography`, `better-colors`, `better-accessibility`), **`msitarzewski/agency-agents`** (`UI Designer`, `UX Architect`, `Whimsy Injector`, `UI Finish-Gate Reviewer`) và bộ đôi **`claude-design` + `popular-web-designs`** của Hermes.

## When to Use

- Thiết kế hoặc hoàn thiện dashboard, workspace, landing page và design system.
- Chuyển báo cáo có sẵn thành giao diện web có bộ lọc/chi tiết, hoặc xuất link preview Vercel.
- Kiểm tra hierarchy, legibility, responsive layout và trạng thái snapshot/live trước khi bàn giao.

## 1. Quy Tắc Bề Mặt Trước Tiên (Surface-First Composition Law)
Trước khi chọn màu hay font, **BẮT BUỘC** tuyên bố rõ giao diện thuộc **1 trong 7 Archetype bề mặt** để triệt tiêu bố cục rập khuôn "Centered Hero + 3 Feature Cards":
1. **Decide / Learn (Landing Page, Marketing, Sales Page):** Thuyết phục & chuyển đổi. Chỉ bề mặt này mới dùng Hero Section + Above-the-Fold Value Proposition + Bento Feature Grid + Social Proof + CTA.
2. **Monitor (Analytics, Dashboard, Telemetry):** Ưu tiên mật độ thông tin (Data Density), phân cấp quét mắt nhanh (Glanceable Hierarchy), sparklines, trạng thái thời gian thực. **Cấm** dùng Hero quảng cáo.
3. **Operate (Workspace, Console, CRM, Kanban):** Ưu tiên phím tắt, trạng thái chọn (Selection State), thanh công cụ thao tác nhanh và phản hồi tức thì.
4. **Compare (Pricing, Plan Matrix, Spec Table):** Căn cột thẳng hàng tuyệt đối, làm nổi bật 1 gói khuyên dùng (Recommended Anchor), ẩn thông số phụ vào accordion/tooltip.
5. **Configure (Settings, Onboarding Wizard, Form):** Tiết lộ tuần tự (Progressive Disclosure), kiểm tra lỗi inline tức thì, ít trang trí.
6. **Explore (Catalog, Gallery, Marketplace, Template Library):** Bộ lọc facet, lưới kết quả đồng nhất, xem trước nhanh (Quick Peek Modal/Drawer).
7. **Command / Inspect (Command Palette `⌘K`, Detail Inspector, DevTools):** Tốc độ bàn phím, độ trễ bằng 0, hiển thị thuộc tính dạng key-value sắc nét.

## 2. Hệ Thống Typography, Màu Sắc OKLCH & Lưới Không Gian (Spatial & Visual Tokens)
- **Typography Scale (3 tầng nghiêm ngặt):**
  - `Display / Hero`: `clamp(2.5rem, 5vw, 4.5rem)`, `line-height: 1.04 - 1.1`, `letter-spacing: -0.03em`, `text-wrap: balance`.
  - `Section / Card Title`: `1.25rem - 2rem`, `line-height: 1.2`, `letter-spacing: -0.02em`.
  - `Body / UI Copy`: `0.9375rem - 1.0625rem` (`15px - 17px`), `line-height: 1.6`, độ dài dòng tối ưu `55ch - 70ch`, `text-wrap: pretty`.
  - `Monospace / Telemetry`: Dùng `JetBrains Mono` hoặc `Geist Mono` với `font-variant-numeric: tabular-nums` cho mọi con số, giá tiền, bộ đếm và mã code.
- **Hệ Màu OKLCH & Độ Tương Phản WCAG AAA/AA:**
  - Tối đa **1 màu nhấn chính (Primary Accent)** + **1 màu ngữ nghĩa phụ**; 85% diện tích phải là dải màu trung tính có sắc độ nhẹ (`Surface-0`, `Surface-1`, `Surface-2`, `Ink-Primary`, `Ink-Muted`, `Border-Hairline`).
  - Đường viền (Border): Ưu tiên `1px solid rgba(255,255,255,0.08)` (Dark mode) hoặc `1px solid rgba(15,23,42,0.08)` (Light mode) thay vì đổ bóng dày nặng nề.
- **Nhịp Không Gian 8pt & Bento Grid Bất Đối Xứng:**
  - Mọi khoảng cách (`padding`, `gap`, `margin`) tuân thủ bội số `4px / 8px` (`8, 12, 16, 24, 32, 48, 64, 96px`).
  - Thay thế lưới 3 cột bằng nhau nhàm chán bằng **Asymmetric Bento Grid** (ví dụ: 1 ô lớn `col-span-7` chứa Interactive Demo + 1 ô `col-span-5` chứa Metric/Diagram, hàng dưới đảo chiều `5-7`).

## 3. Quy trình xuất bản Dashboard / Preview

1. **Tái sử dụng dữ liệu thật trước khi thiết kế:** đọc báo cáo hiện có, xuất đúng số dòng duy nhất, giữ N/A là thiếu dữ liệu; không bịa chart, thành tích hoặc thời gian cập nhật.
2. **Phân biệt snapshot và live ngay trên giao diện:** hiện thời điểm dữ liệu nguồn; đánh dấu đầu ra mô hình chưa kiểm chứng và các giả định trọng yếu. Hosting không đồng nghĩa tự cập nhật định kỳ.
3. **Giữ phạm vi bản xem trước gọn:** dùng HTML/CSS/JS tĩnh khi chỉ cần xem, lọc và tải báo cáo; tách thư mục upload và project preview khỏi ứng dụng đang hoạt động.
4. **Xác minh trước khi gửi link:** kiểm tra manifest upload không chứa `.env*`/credentials, trạng thái deployment, HTTP công khai không đăng nhập, rồi chạy UI trên desktop và mobile tại URL cuối. Dùng `webapp-testing` cho thao tác trình duyệt.
5. **Kiểm tra mobile bằng số đo, không chỉ screenshot:** đối chiếu screen/viewport/document width, giữ bảng cuộn ngang bên trong vùng riêng; chứa các nhãn `.sr-only` tuyệt đối trong scroll container bằng `position: relative` khi chúng làm document phình ngang.
6. **Bàn giao link trước, ghi chú sau:** khi người dùng xin link xem trước, mở đầu bằng URL đã xác minh và mô tả ngắn phần xem được; nói rõ snapshot/live và phần tự động hóa chưa kết nối, không lặp lại toàn bộ kế hoạch triển khai.

Đọc `references/static-preview-deployment.md` khi xuất report/dashboard lên Vercel: discovery scope → link project → dry-run upload manifest → browser QA → deploy → read-back URL công khai.

## 4. Bộ Kiểm Định 10 Dấu Hiệu AI-Slop (`Slop_Diagnostic_Score <= 1/10`)
Trước khi bàn giao code HTML/React/Tailwind hoặc Design System, phải tự chấm điểm 10 lỗi AI-Slop (mỗi lỗi = +1 điểm; bắt buộc đạt **`<= 1/10`**):
1. `Tech Gradient Slop`: Nền hoặc chữ phủ gradient tím-xanh-hồng loè loẹt vô nghĩa.
2. `Default Indigo Hue`: Dùng màu `#6366f1` / `#8b5cf6` mặc định của Tailwind khi thương hiệu không yêu cầu.
3. `Equal 3-Card Feature Grid`: 3 thẻ giống hệt nhau (Icon tròn + Tiêu đề + 2 dòng chữ) lặp đi lặp lại.
4. `Left-Border Callout Card`: Thẻ có viền trái dày 4px màu mè kiểu văn bản AI sinh tự động.
5. `Unearned Glassmorphism`: Lạm dụng `backdrop-filter: blur()` chồng chéo gây đục chữ và tụt FPS.
6. `Fake Monument Stats`: Bịa ra các con số vô hồn kiểu `99.9% Uptime | 10M+ Users | 24/7 Support` không có ngữ cảnh thật.
7. `Centered Icon Topper`: Đặt icon trong ô vuông bo góc căn giữa phía trên mọi tiêu đề.
8. `Center-Stack Everything`: Căn giữa toàn bộ văn bản dài làm mắt người đọc mất điểm neo trái.
9. `Unstyled Inter Default`: Dùng font mặc định không tinh chỉnh `letter-spacing`, `font-feature-settings`, hoặc không phối cặp font có chủ đích (tham chiếu 54 hệ thống trong `popular-web-designs` như Linear, Stripe, Vercel, Anthropic Claude, Apple, Framer).
10. `Wrong Surface Archetype`: Nhét Hero quảng cáo vào màn hình Dashboard/App hoặc nhét bảng thông số thô vào màn hình Landing Page.
