---
name: risk-guard
description: "Hard Risk Guardrails, Position Sizing Calculator & Emergency Kill Switch for Ai trading. Enforces max risk per trade (<= 2%), minimum R:R ratio (>= 1.5), max leverage (<= 5x), and daily drawdown circuit breaker (<= 4%). Always run risk-guard size before proposing or executing any trade."
version: 1.0.0
author: Integrated for Hermes Agent — Ai trading
license: MIT
platforms: [macos, linux, windows]
metadata:
  tags: [risk-guard, position-sizing, kill-switch, circuit-breaker, risk-management, rr-ratio]
  hermes:
    tags: [RiskGuard, PositionSizing, KillSwitch, CircuitBreaker]
    related_skills: [vibetrading, freqtrade, trade-journal]
---

# Risk Guard (`risk-guard` — Cầu Dao Quản Trị Rủi Ro & Tính Khối Lượng Lệnh)

- **Executable CLI:** `/Users/buithiphuongthao/.local/bin/risk-guard`
- **Source Script:** `/Users/buithiphuongthao/.hermes/profiles/ai-trading/tools/risk_guard.py`
- **State File:** `/Users/buithiphuongthao/.hermes/profiles/ai-trading/workspace/risk_guard_state.json`

## Các Lệnh Bắt Buộc Trước Khi Đề Xuất Lệnh

```bash
# 1. Tính khối lượng lệnh chuẩn theo % rủi ro & Kiểm tra duyệt an toàn (R:R >= 1.5, Leverage <= 5x, Risk <= 2%)
/Users/buithiphuongthao/.local/bin/risk-guard size \
  --balance 10000 \
  --risk-pct 1.0 \
  --entry 90000 \
  --sl 88200 \
  --tp 94500 \
  --leverage 3

# 2. Kiểm tra trạng thái cầu dao rủi ro hiện tại
/Users/buithiphuongthao/.local/bin/risk-guard status

# 3. Bật / Tắt cầu dao ngắt mạch khẩn cấp (Kill Switch)
/Users/buithiphuongthao/.local/bin/risk-guard kill-switch --on --reason "Biến động tin tức FOMC"
/Users/buithiphuongthao/.local/bin/risk-guard kill-switch --off
```
