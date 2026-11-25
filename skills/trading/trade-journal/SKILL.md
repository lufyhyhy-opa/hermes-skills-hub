---
name: trade-journal
description: "SQLite Trade Journal & Post-Mortem Memory Ledger for Ai trading. Logs every recommended trade signal (Entry, SL, TP, Leverage, Thesis), evaluates open signals against real-time Binance/CCXT prices to check TP/SL hits and unrealized PnL, and records post-mortem lessons learned."
version: 1.0.0
author: Integrated for Hermes Agent — Ai trading
license: MIT
platforms: [macos, linux, windows]
metadata:
  tags: [trade-journal, post-mortem, trading-ledger, pnl-tracker, signal-evaluation]
  hermes:
    tags: [TradeJournal, PostMortem, PnLTracker, SignalLedger]
    related_skills: [crypto-radar, risk-guard, vibetrading]
---

# Trade Journal (`trade-journal` — Sổ Cái Nhật Ký Kèo & Tự Kiểm Điểm Sau Giao Dịch)

- **Executable CLI:** `/Users/buithiphuongthao/.local/bin/trade-journal`
- **Source Script:** `/Users/buithiphuongthao/.hermes/profiles/ai-trading/tools/trade_journal.py`
- **Database:** `/Users/buithiphuongthao/.hermes/profiles/ai-trading/workspace/trade_journal.db`

## Các Lệnh Quản Lý Sổ Cái Giao Dịch

```bash
# 1. Ghi nhận một kèo / vị thế mới vào sổ cái
/Users/buithiphuongthao/.local/bin/trade-journal log \
  --symbol BTC/USDT \
  --side LONG \
  --entry 90000 \
  --sl 88200 \
  --tp 94500 \
  --qty 0.055 \
  --leverage 3 \
  --source "TradingAgents + CryptoRadar" \
  --thesis "RSI 1h quá bán + Funding Rate âm trên Hyperliquid"

# 2. Chấm điểm tự động tất cả các kèo đang OPEN so với giá thị trường thời gian thực
/Users/buithiphuongthao/.local/bin/trade-journal evaluate

# 3. Đóng kèo và ghi lại bài học rút kinh nghiệm (Post-Mortem Lesson)
/Users/buithiphuongthao/.local/bin/trade-journal close \
  --id 1 \
  --exit-price 94500 \
  --lesson "Điểm vào hợp lưu EMA50 khung 4h rất chuẩn, giữ đúng kỷ luật TP."

# 4. Xem thống kê Win Rate, Avg PnL và danh sách bài học xương máu
/Users/buithiphuongthao/.local/bin/trade-journal stats
```
