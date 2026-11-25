---
name: freqtrade
description: "Freqtrade (freqtrade/freqtrade v2026.11 + FreqUI 3.3.0 + TA-Lib) — 24/7 Crypto Automated Trading Bot, Backtesting, Hyperopt & FreqAI Machine Learning Engine. Use when downloading historical OHLCV data, backtesting IStrategy files, running hyperparameter optimization (hyperopt), or launching 24/7 dry-run / live trading with FreqUI dashboard at http://127.0.0.1:8089."
version: 2026.11.0
author: Freqtrade Team (Integrated for Hermes Agent — Ai trading)
license: GPL-3.0
platforms: [macos, linux, windows]
metadata:
  tags: [freqtrade, frequi, crypto-bot, hyperopt, freqai, backtest, dry-run, 24-7-trading]
  hermes:
    tags: [Freqtrade, FreqUI, CryptoBot24x7, Hyperopt, FreqAI]
    related_skills: [vibetrading, hkuds-vibe-trading, tradingagents, crypto-radar, risk-guard]
---

# Freqtrade (`freqtrade/freqtrade` — 24/7 Crypto Trading Bot + FreqUI + FreqAI)

- **Repository Root:** `/Users/buithiphuongthao/.hermes/freqtrade`
- **Dedicated Python Venv:** `/Users/buithiphuongthao/.hermes/freqtrade/.venv/bin/python`
- **Global CLI Executable:** `/Users/buithiphuongthao/.local/bin/freqtrade`
- **User Data Workspace:** `/Users/buithiphuongthao/.hermes/profiles/ai-trading/workspace/freqtrade_user_data`
- **Default Config (Dry-Run + FreqUI):** `/Users/buithiphuongthao/.hermes/profiles/ai-trading/workspace/freqtrade_user_data/config.json`
- **Strategies Directory:** `/Users/buithiphuongthao/.hermes/profiles/ai-trading/workspace/freqtrade_user_data/strategies/`
- **FreqUI Web Dashboard:** `http://127.0.0.1:8089` (User: `aitrading` / Pass: `aitrading123`)

---

## 1. Các lệnh CLI Thường Dùng (`freqtrade`)

```bash
# 1. Tải dữ liệu nến lịch sử (Binance: BTC/USDT, ETH/USDT, SOL/USDT...)
/Users/buithiphuongthao/.local/bin/freqtrade download-data \
  --config /Users/buithiphuongthao/.hermes/profiles/ai-trading/workspace/freqtrade_user_data/config.json \
  --timeframes 15m 1h 4h --days 30

# 2. Chạy Backtest chiến lược
/Users/buithiphuongthao/.local/bin/freqtrade backtesting \
  --config /Users/buithiphuongthao/.hermes/profiles/ai-trading/workspace/freqtrade_user_data/config.json \
  --strategy SampleStrategy --timeframe 1h

# 3. Tạo mới 1 file chiến lược từ template
/Users/buithiphuongthao/.local/bin/freqtrade new-strategy \
  --userdir /Users/buithiphuongthao/.hermes/profiles/ai-trading/workspace/freqtrade_user_data \
  --strategy MyCustomStrategy

# 4. Chạy Bot 24/7 ở chế độ Dry-Run (Paper Trading) kèm giao diện Web FreqUI tại http://127.0.0.1:8089
/Users/buithiphuongthao/.local/bin/freqtrade trade \
  --config /Users/buithiphuongthao/.hermes/profiles/ai-trading/workspace/freqtrade_user_data/config.json \
  --strategy SampleStrategy
```
