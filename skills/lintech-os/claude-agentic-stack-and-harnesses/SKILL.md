---
name: claude-agentic-stack-and-harnesses
description: "Hệ quy chiếu Kiến Trúc Tác Nhân Tự Trị của Anthropic & Kho 240+ GitHub Claude Code (tổng hợp từ @kevindatas / Anthropic Research: Building Effective Agents, Effective Harnesses for Long-Running Agents, Claude Agent SDK Python/TS, Hooks, Subagents, Memory, 19 Official Anthropic Skills & Awesome Claude Code). Sử dụng khi thiết kế hệ thống multi-agent, chạy dự án dài hạn qua hermes-long-horizon-harness, tích hợp Claude Agent SDK hoặc tra cứu kho công cụ GitHub đã cài sẵn trên máy."
version: 1.0.0
author: LinTech Autonomous Council
license: MIT
metadata:
  hermes:
    tags: [anthropic, claude-code, agent-sdk, long-running-agents, hooks, subagents, awesome-claude-code, multi-agent-architecture]
    category: lintech-os
---

# 🏛️ Kiến Trúc Tác Nhân Tự Trị Anthropic & Kho GitHub Claude Code (`claude-agentic-stack-and-harnesses`)

> **Luận điểm chiến lược (Eric Schmidt — Cựu CEO Google / Bài tổng hợp của `@kevindatas`):**
> *"Con đường trực diện nhất để xây dựng doanh nghiệp giá trị lớn trong 2 năm tới là tạo ra một công ty AI Tác nhân (Agentic AI Company). Hãy phát triển một Agent giải quyết trọn vẹn một bài toán thực tế tốt hơn bất kỳ ai khác — bạn có thể vận hành cả một doanh nghiệp thực thụ với đội ngũ Agent tự trị."*

---

## 1. Bản Đồ 5 Kho GitHub Cốt Lõi & 19 Official Anthropic Skills Đã Cài Đặt Trên Máy

Toàn bộ các kho mã nguồn GitHub từ bài viết đã được clone sẵn tại **cả 2 nơi** để 19 Agent của Hermes và các dự án trong Workspace sử dụng offline/trực tiếp bất cứ lúc nào:

- **Thư mục trong Hermes:** `/Users/buithiphuongthao/.hermes/installs/claude-agentic-repos/`
- **Thư mục trong Workspace:** `/Users/buithiphuongthao/Desktop/AI/thư mục không có tiêu đề/claude-agentic-repos/`

| # | Kho GitHub (`owner/repo`) | Đường dẫn cài đặt trên máy | Ứng dụng thực chiến trong tương lai |
|---|---|---|---|
| **1** | **`anthropics/claude-agent-sdk-python`** | `~/.hermes/installs/claude-agentic-repos/claude-agent-sdk-python` | Xây dựng Agent tự trị bằng Python dùng chung động cơ vòng lặp công cụ (agentic loop), quản lý tiến trình và MCP của Claude Code. |
| **2** | **`anthropics/claude-agent-sdk-typescript`** | `~/.hermes/installs/claude-agentic-repos/claude-agent-sdk-typescript` | Nhúng Claude Agent trực tiếp vào ứng dụng Web/Next.js/Node.js (`query()`, custom tools, streaming messages, permission callbacks). |
| **3** | **`anthropics/claude-code-action`** | `~/.hermes/installs/claude-agentic-repos/claude-code-action` | Tự động hóa GitHub PR & Issues: gắn Agent vào CI/CD để tự viết code, tự review PR và tự sửa lỗi khi test fail. |
| **4** | **`anthropics/skills` (19 Official Skills)** | `~/.hermes/shared-skills/anthropics/` & `.agents/skills/` | 19 kỹ năng chính chủ Anthropic: `claude-api`, `frontend-design`, `mcp-builder`, `webapp-testing`, `web-artifacts-builder`, `pptx`, `docx`, `pdf`, `xlsx`, `canvas-design`, `theme-factory`, `algorithmic-art`, `doc-coauthoring`, `skill-creator`, `brand-guidelines`, `internal-comms`, `slack-gif-creator`, `discernment-nudge`, `academy-guide`. |
| **5** | **`hesreallyhim/awesome-claude-code`** | `~/.hermes/installs/claude-agentic-repos/awesome-claude-code` | Danh bạ **240 kho GitHub chọn lọc** về Agent Orchestration, Hooks, Memory, Linting, Testing, Status Lines, Security & UI/UX. |

---

## 2. Tinh Hoa Kiến Trúc Tác Nhân Từ Nghiên Cứu Của Anthropic

### 2.1. 5 Mẫu Thiết Kế Hệ Thống Tác Nhân (*Building Effective Agents* — `anthropic.com/research/building-effective-agents`)
Nguyên tắc số 1 của Anthropic: **Bắt đầu từ giải pháp đơn giản nhất, chỉ tăng độ phức tạp khi thực sự cần thiết. Ưu tiên Workflows tất định trước, Autonomous Agents có kiểm soát sau:**
1. **Prompt Chaining (Chuỗi bước tuần tự có cổng kiểm tra):** Chia tác vụ lớn thành chuỗi bước cố định; giữa các bước có **Gate kiểm tra bằng code** (nếu bước $k$ chưa đạt chuẩn thì chặn ngay trước khi sang bước $k+1$).
2. **Routing (Phân luồng chuyên biệt):** Phân loại đầu vào và điều hướng thẳng tới Agent/Skill chuyên trách (`agent-01` → `agent-18`, `ai-trading`).
3. **Parallelization (Song song hóa — Sectioning & Voting):** Chia nhỏ công việc độc lập chạy song song hoặc cho nhiều góc nhìn bỏ phiếu (như `Tree of Thoughts` 3 phương án của Hội đồng Hermes).
4. **Orchestrator-Workers (Tổng chỉ huy & Đội đặc nhiệm):** `agent-00-orchestrator` tự động bóc tách bài toán động, giao việc cho các Worker Agent và tổng hợp kết quả.
5. **Evaluator-Optimizer (Người viết & Giám khảo độc lập):** Tách rời hoàn toàn Agent sinh nội dung/code (`agent-04`, `agent-17`) khỏi Agent chấm điểm và bắt lỗi (`agent-05-quality-gate`, `hermes-verify-harness`).

### 2.2. Khung Điều Phối Cho Tác Nhân Chạy Dài Hạn (*Effective Harnesses for Long-Running Agents* — `anthropic.com/engineering/effective-harnesses-for-long-running-agents`)
Khi một dự án kéo dài qua nhiều phiên làm việc (multi-hour / multi-day sessions), các Agent thường mắc 2 bệnh chí mạng: **(1) Ôm đồm làm một lúc quá nhiều thứ dẫn đến cạn context giữa chừng**, hoặc **(2) Nhìn thấy một vài tính năng đã có rồi vội vàng tuyên bố dự án đã hoàn thành 100%**.

Giải pháp chuẩn của Anthropic (đã được cài thành công cụ CLI toàn cục `/Users/buithiphuongthao/.local/bin/hermes-long-horizon-harness`):
1. **Mô hình 2 Tác Nhân (`Initializer Agent` + `Incremental Coding Agent`):**
   - **Pha Khởi Tạo (`Initializer Agent`):** Phân rã toàn bộ yêu cầu dự án thành sổ cái JSON bất biến **`feature_list.json`** (dùng định dạng JSON kèm `immutable_spec_hash` thay vì Markdown để ngăn Agent tự ý xóa hoặc sửa đổi tiêu chí nghiệm thu) và khởi tạo nhật ký bàn giao **`claude-progress.txt`**.
   - **Pha Thực Thi Tăng Trưởng (`Incremental Coding Agent`):** Mỗi phiên/vòng lặp chỉ lấy **đúng 1 tính năng** tiếp theo có `"passes": false`, thực thi trọn vẹn, chạy kiểm chứng thực tế (`hermes-verify-harness`), rồi mới đánh dấu `"passes": true` và ghi nhật ký vào `claude-progress.txt`.
2. **Cách gọi CLI `hermes-long-horizon-harness` trong mọi dự án lớn:**
   ```bash
   # 1. Khởi tạo sổ cái tính năng bất biến cho dự án dài hạn
   /Users/buithiphuongthao/.local/bin/hermes-long-horizon-harness init <thư_mục_dự_án> --goal "<Mục tiêu dự án>"

   # 2. Kiểm tra trạng thái & lấy đúng 1 tính năng tiếp theo cần làm
   /Users/buithiphuongthao/.local/bin/hermes-long-horizon-harness status <thư_mục_dự_án>

   # 3. Hoàn thành tính năng (tự động chạy hermes-verify-harness trước khi cho phép đổi passes=true)
   /Users/buithiphuongthao/.local/bin/hermes-long-horizon-harness complete <thư_mục_dự_án> --id F001 --note "Đã xác thực 0 lỗi"
   ```

### 2.3. 4 Trụ Cột Thực Thi Của Claude Code (`Best Practices`, `Hooks`, `Sub-agents`, `Memory`)
1. **Hooks Tất Định (`PreToolUse` / `PostToolUse` / `Stop`):**
   - Không dựa vào lời dặn trong prompt nếu bạn cần quy tắc thực thi 100% số lần. Dùng Hooks hoặc CLI Verifier (`hermes-verify-harness`) để tự động chạy linter/formatter ngay sau mỗi lần sửa file và chặn báo cáo hoàn thành nếu kiểm chứng còn lỗi.
2. **Subagents Chuyên Biệt & Cô Lập Context:**
   - Dùng Subagents cho các tác vụ nghiên cứu sâu, đọc log lớn, hoặc chạy kiểm thử độc lập để giữ cho cửa sổ ngữ cảnh (context window) của Orchestrator luôn sạch và tập trung.
3. **Bộ Nhớ Phân Tầng Tinh Gọn (`SOUL.md` / `MEMORY.md` / `CLAUDE.md`):**
   - Chỉ lưu các lệnh build/verify chuẩn, ràng buộc kiến trúc tối kỵ và khẩu vị thực tế của người dùng. Tránh biến file bộ nhớ thành bãi rác văn xuôi dài dòng.
4. **Quy Trình Explore $\rightarrow$ Plan $\rightarrow$ Verify-First $\rightarrow$ Code $\rightarrow$ Commit:**
   - Đọc mã nguồn thật trước khi lập kế hoạch $\rightarrow$ Viết tiêu chí kiểm chứng trước $\rightarrow$ Code $\rightarrow$ Tự chạy Verifier để chứng minh kết quả.
