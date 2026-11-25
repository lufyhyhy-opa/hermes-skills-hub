---
name: hy-memory
description: "Dual-system (System 1 + System 2) 8-layer cognitive long-term memory for Hermes Agent powered by Tencent-Hunyuan/Hy-Memory and HyAtlas-Memory (hyatlas-go). Provides Chat Memory (8 layers: L1 Profile, L2 Raw, L3 Atomic Facts, L4 Episode Summaries, L5 Knowledge, L6 Schemas, L7 Prospective Intentions, L8 Entity Pages), Working Memory, Coding Memory (diff-chains), and a Bitemporal Knowledge Graph with local BGE embeddings and gpt-6.1-sol consolidation."
version: 2.0.16
author: Tencent Hunyuan & HyAtlas (Integrated for Hermes Agent & LinTech OS)
license: Apache-2.0
platforms: [macos, linux, windows]
metadata:
  tags: [memory, hy-memory, hyatlas, long-term-memory, knowledge-graph, system1-system2, bge, cognitive-memory]
  hermes:
    tags: [HyMemory, HyAtlas, CognitiveMemory, LongTermMemory, KnowledgeGraph]
    related_skills: [using-superpowers, brainstorming, writing-plans]
---

# Hy-Memory & HyAtlas-Memory (`Tencent-Hunyuan/Hy-Memory` × `tuancookiez-hub/HyAtlas-Memory`)

Hệ thống bộ nhớ dài hạn nhận thức 8 tầng (System 1 + System 2 Cognitive Memory) đã được cài đặt và kích hoạt trực tiếp cho toàn bộ **19 Agent Hermes (`agent-00` → `agent-18`)**.

## 1. Thành phần đã cài đặt trên hệ thống
- **Binary Server 8 tầng (`hyatlas-go` v5.0.0 — macOS ARM64)**: `/Users/buithiphuongthao/.local/bin/hyatlas-go` (tích hợp sẵn mô hình vector `BGE-small-en-v1.5` ONNX nội bộ + kết nối LLM `gpt-6.1-sol` ở chế độ `ultra`).
- **Hermes Memory Provider Plugin**:
  - `/Users/buithiphuongthao/.hermes/plugins/hyatlas` (`memory.provider: hyatlas`, chạy trên `http://127.0.0.1:19528`)
  - `/Users/buithiphuongthao/.hermes/plugins/hy_memory` (Official Tencent Hunyuan MemHub recall provider)
- **Hermes Desktop UI Pane**: `/Users/buithiphuongthao/.hermes/desktop-plugins/hyatlas/plugin.js`
- **Python SDK (`hy_memory`)**: `/Users/buithiphuongthao/.hermes/shared-skills/ai-engineering/hy-memory/hy_memory`

## 2. Bộ 4 Công Cụ Bộ Nhớ Dài Hạn (Agent Memory Tools)
Khi `memory.provider: hyatlas` hoạt động, mọi Agent trong Hermes có thể sử dụng trực tiếp:
1. **`hyatlas_search`**: Tìm kiếm ký ức đa kênh (`pages`, `profile`, `proactive`, `experiences`, `normal`) theo ngữ nghĩa (BGE vector) + từ khóa.
2. **`hyatlas_add`**: Ghi nhớ chủ động một sự kiện, quy tắc thương hiệu, quyết định kỹ thuật hoặc sở thích của Giám đốc vào bộ nhớ 8 tầng.
3. **`hyatlas_recent`**: Xem các ký ức vừa được trích xuất gần đây.
4. **`hyatlas_status`**: Kiểm tra trạng thái server bộ nhớ, số lượng thực thể trong từng tầng (L1 → L8) và Knowledge Graph.

## 3. Kiến trúc 8 Tầng Ký Ức (8-Layer Cognitive Hierarchy)
- **L1 — Profile**: Hồ sơ cá nhân, phong cách làm việc và sở thích lâu dài của người dùng.
- **L2 — Raw**: Toàn bộ lịch sử hội thoại gốc giữa người dùng và các Agent.
- **L3 — Atomic Facts**: Các sự kiện nguyên tử có gắn mốc thời gian (`happened YYYY-MM-DD`) và đối chiếu thay thế (`was: ...`).
- **L4 — Episode Summaries**: Tóm tắt theo từng phiên/chủ đề công việc.
- **L5 — Knowledge**: Tri thức miền chuyên môn được đúc kết qua nhiều phiên.
- **L6 — Schemas**: Khuôn mẫu tư duy và quy luật hành vi lặp lại.
- **L7 — Prospective Intentions**: Các dự định, kế hoạch đang dang dở hoặc việc cần làm trong tương lai.
- **L8 — Entity Pages**: Trang hồ sơ thực thể (dự án, thương hiệu, nhân sự, khách hàng) trong đồ thị tri thức (Bitemporal Knowledge Graph).

## 4. Lệnh quản trị nhanh qua CLI / Slash Command
- Kiểm tra sức khỏe toàn diện:
  ```bash
  hermes hyatlas doctor
  hermes hyatlas status
  ```
- Tìm kiếm hoặc thêm ký ức từ CLI:
  ```bash
  hermes hyatlas search "chiến lược marketing"
  hermes hyatlas add "Tất cả 19 Agent luôn sử dụng model gpt-6.1-sol"
  ```
- Trong khung chat Hermes Desktop: dùng lệnh `/hyatlas status`, `/hyatlas search <từ_khóa>`, `/hyatlas recent`.
