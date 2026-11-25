---
name: vibe-coding-course
description: Use when applying the saved Vibe Coding course.
---

# Vibe Coding — quy trình khóa học đã lưu

Dùng khi người dùng nhắc khóa Vibe Coding, lộ trình sáu tháng, hoặc muốn xây web/app/automation theo khóa này. Không áp toàn khóa cho việc nhỏ không liên quan. Đọc [course-guide](references/course-guide.md) khi cần lộ trình, nguyên tắc và lưu ý nguồn.

## Quy trình thực thi

1. **Explore:** đọc repo, rules, docs, tests và git diff trước khi sửa. Giữ stack hiện có. Web mới chưa chọn stack: đề xuất Next.js App Router + TypeScript + Tailwind + Supabase + Vercel.
2. **PRP → PRD:** xác định người dùng mục tiêu, vấn đề cốt lõi và tiêu chí thành công kiểm thử được. Với dự án bảo trì lâu dài, đội từ hai người, hoặc hành vi nhạy cảm kinh doanh/pháp lý: dùng SDD, đặc tả hành vi → requirements → thiết kế → triển khai → validation. Lưu quyết định trong repo.
3. **Plan → duyệt:** nêu file/hàm cần tạo hoặc sửa, dependencies, ngoại lệ, kiến trúc, test và rủi ro. Chờ duyệt kế hoạch trước triển khai; kế hoạch không tự cấp quyền deploy.
4. **Chia nhỏ:** thường chia tính năng thành 3–5 nhiệm vụ. Mỗi prompt có **Goal, Context, Constraints, Output Format**. Context chỉ rõ file/API/component mẫu; Constraints nêu phạm vi sửa và vùng cấm; Output nêu artifact và bằng chứng kiểm thử.
5. **Implement:** orchestrator giao lập trình/thiết kế cho chuyên gia thực sự khả dụng, không giả lập agent hoặc tự làm thay. Thiếu chuyên gia/công cụ: báo rõ. TDD theo từng hành vi: viết test → chạy thấy fail đúng lý do → code tối thiểu → pass → refactor.
6. **Independent Review → Fix → Verify:** reviewer/ngữ cảnh mới kiểm tra spec, logic nghiệp vụ, bảo mật, package có thật. Không gọi tự review là review độc lập. Sửa rồi chạy lại tests, lint/typecheck/build phù hợp và luồng người dùng thực. Thiếu reviewer phải báo rõ, không tuyên bố đã qua.
7. **Commit/Ship:** kiểm tra diff, checkpoint trạng thái tốt trong quyền được cấp. Push, merge, deploy hoặc ghi hệ thống ngoài chỉ khi được ủy quyền; đọc lại đích sau khi ghi ngoài. Báo artifact, lệnh và kết quả thực, phần chưa kiểm chứng. Giữ nguyên mọi HITL gate đang áp dụng.

## Context và chống Doom Loop

Duy trì docs/architecture, feature specs, rules và Common AI Mistakes. Tham chiếu component sẵn có; tra tài liệu chính thức/llms.txt đúng phiên bản khi cần API. Context dài hoặc chuyển tính năng: bàn giao ngắn rồi mở phiên mới.

Lấy lỗi thật, log đã che bí mật và ca tái hiện; kiểm tra giả thuyết bằng test. **Ba lần sửa thất bại: dừng, xem lại prompt/spec/nguyên nhân; không thử mù lần thứ tư.**

## Cổng an toàn

Secrets phía server qua env, gitignore trước push; kiểm tra validation server, auth/authorization, RLS, CORS, dependency và prompt injection. Thiếu RLS cần thiết: dừng xin quyết định, không công khai dữ liệu.

Tách dev/prod; migration có backup/rollback, không thử trên dữ liệu thật. Trước public launch: monitoring lỗi/LLM, token/chi phí, quota/rate limit và cảnh báo; xác minh budget dashboard là hard cap hay chỉ cảnh báo.

Figma: trích design tokens trước component. Mobile: cân nhắc React Native + Expo + Expo Router, kiểm tra dependency và thiết bị/emulator thật.

## Ví dụ prompt

Goal: tạo login tại `app/login/page.tsx`. Context: đọc Supabase client hiện có ở `lib/supabase.ts`, lấy form `app/signup/page.tsx` làm mẫu nếu các file này thực sự tồn tại. Constraints: email/password, xử lý invalid credentials; không sửa ngoài phạm vi đã duyệt. Output Format: component, test hành vi và kết quả chạy thật. Đây là ví dụ khóa, không giả định đường dẫn tồn tại trong repo người dùng.

## Nguồn

https://docs.google.com/document/d/1wpGrujdJ7f3SfcguBeTT1WjPfQkLLsjjO_wBnoPxEQY/mobilebasic?#heading=h.1btyyboke51h

Toàn văn đã tải trong workspace: `/Users/buithiphuongthao/Desktop/chatbot/vibe-coding-course-source.txt`; HTML giữ liên kết: `/Users/buithiphuongthao/Desktop/chatbot/vibe-coding-course-source.html`. Đây là bản nguồn tham khảo, không phải bằng chứng đã xem các video liên kết. Giá/phiên bản/model/lệnh cài đặt cần kiểm tra lại từ tài liệu chính thức khi dùng.
