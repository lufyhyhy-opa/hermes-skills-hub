---
name: lintech-copy-engine
description: "Use when outlining, writing, humanizing, scoring (LLM Judge 0-10), or repurposing text posts, Threads, and 6-7 slide Carousels. Integrates coreyhaines31/marketingskills (Seven Sweeps, Hook Formulas, No AI Tells) with blader/humanizer."
version: 2.0.0
author: LinTech Content OS × coreyhaines31/marketingskills × blader/humanizer
license: MIT
metadata:
  hermes:
    tags: [copywriting, copy-editing, seven-sweeps, llm-judge, threads, carousel, anti-ai-slop]
    category: creative
---

# Động Cơ Sản Xuất Chữ, Khử Mùi AI & Giám Khảo Chấm Điểm (`lintech-copy-engine`)

## 1. Luật Cấm Tuyệt Đối "No AI Tells" (Trừ 1.5 điểm/lỗi)
- Cấm cấu trúc lật câu Contrast Reveals: *"Không phải X, mà là Y"*, *"Nó không chỉ là X; nó còn là Y"*.
- Cấm liệt kê phủ định Negation Lists: *"Không cần code, không tốn phí, không mất thời gian."*
- Cấm tự hỏi tự trả lời: *"Kết quả là gì ư? Nhanh gấp 3 lần."*
- Cấm từ vựng sáo rỗng: *"Trong kỷ nguyên số"*, *"hãy cùng khám phá"*, *"đừng lo lắng"*, *"chìa khóa vàng"*, *"bức tranh toàn cảnh"*.

## 2. Quy Trình 7 Sweeps & Chấm Điểm LLM Judge (Agent 05 - Thang 10.0)
- Sweep 1 & 2 (Clarity + Voice & Tone): 0 - 3.0đ
- Sweep 3 & 4 (So What? + Prove It với ẩn dụ đời thường): 0 - 3.0đ
- Sweep 5 & 6 (Specificity + Emotion ở 2 dòng Hook đầu): 0 - 2.0đ
- Sweep 7 (Zero Risk & CTA tự nhiên): 0 - 2.0đ
- **Quy tắc rẽ nhánh:** Điểm `< 8.0` (tối đa 2 vòng) -> `REJECT_AND_REWRITE`. Điểm `>= 8.0` -> `APPROVED`.
