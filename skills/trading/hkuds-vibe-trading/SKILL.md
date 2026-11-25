---
name: hkuds-vibe-trading
description: "HKUDS/Vibe-Trading (vibe-trading-ai v0.1.19) — Multi-Agent Finance & Crypto Trading Workspace, Alpha Zoo (478 alphas across 5 libraries), Swarm Research Teams (30 presets), Paper Trading & Shadow Account, Options Payoff/IV Lab, and 28 Market-Data Sources (OKX, Binance, CCXT, Yahoo, AKShare). Use when running multi-agent swarm analysis, benchmarking alpha factors, running natural-language backtest reports, paper trading, or MCP integration."
version: 0.1.19
author: HKUDS (Integrated for Hermes Agent — Ai trading)
license: MIT
platforms: [macos, linux, windows]
metadata:
  tags: [vibe-trading-ai, hkuds, alpha-zoo, swarm, crypto-backtest, paper-trading, shadow-account, mcp]
  hermes:
    tags: [HKUDSVibeTrading, AlphaZoo, SwarmTrading, PaperTrading, CryptoResearch]
    related_skills: [vibetrading, tradingagents, research]
---

# HKUDS/Vibe-Trading (`vibe-trading-ai` — Multi-Agent Trading Workspace & Alpha Zoo)

- **Repository Root:** `/Users/buithiphuongthao/.hermes/hkuds-vibe-trading`
- **Dedicated Python Venv:** `/Users/buithiphuongthao/.hermes/hkuds-vibe-trading/.venv/bin/python`
- **Global CLI Executable:** `/Users/buithiphuongthao/.local/bin/vibe-trading`
- **MCP Server Executable:** `/Users/buithiphuongthao/.local/bin/vibe-trading-mcp`
- **Built-in Agent Skills & Alpha Zoo:**
  - Skills: `/Users/buithiphuongthao/.hermes/hkuds-vibe-trading/agent/src/skills/`
  - Alpha Zoo (478 factors): `/Users/buithiphuongthao/.hermes/hkuds-vibe-trading/agent/src/factors/zoo/`
  - Swarm Presets (30 teams): `/Users/buithiphuongthao/.hermes/hkuds-vibe-trading/agent/src/swarm/presets/`

---

## 1. Khi nào sử dụng `hkuds-vibe-trading` (So sánh với `vibetrading`)
- Dùng **`vibetrading` (`VibeTradingLabs/vibetrading`)** khi cần sinh code chiến lược `@vibe` nhanh, kiểm tra tĩnh (`validate`), chạy backtest Perp/Spot tốc độ cao hoặc chạy live trực tiếp trên Hyperliquid/Paradex/Lighter/Aster.
- Dùng **`hkuds-vibe-trading` (`HKUDS/Vibe-Trading`)** khi cần:
  1. **Nghiên cứu Đa Tác Nhân (Swarm Teams):** Phối hợp 30 đội ngũ agent chuyên biệt (Crypto, Quant, Macro, Catalyst, Risk) để phân tích chuyên sâu.
  2. **Alpha Zoo Benchmark:** Chấm điểm và xếp hạng 478 yếu tố định lượng (Alpha101, GTJA191, Qlib158...).
  3. **Báo cáo Nghiên cứu & Backtest bằng Ngôn ngữ Tự nhiên:** Xuất báo cáo HTML/PDF/Markdown có kiểm chứng dữ liệu từ 28 nguồn (OKX, Binance, CCXT, Yahoo Finance...).
  4. **Paper Trading & Shadow Account:** Theo dõi danh mục mô phỏng, đối soát sổ lệnh (`paper_trade_reconcile`) và nhật ký giao dịch.

---

## 2. Các lệnh CLI (`vibe-trading`)

```bash
# Xem hướng dẫn đầy đủ các lệnh của HKUDS Vibe-Trading
/Users/buithiphuongthao/.local/bin/vibe-trading --help

# Chạy prompt nghiên cứu hoặc backtest trực tiếp bằng ngôn ngữ tự nhiên
/Users/buithiphuongthao/.local/bin/vibe-trading run -p "Backtest a BTC-USDT 20/50 moving-average crossover for 2025. Compare it with buy-and-hold and report maximum drawdown."

# Benchmark kho Alpha Zoo (478 alphas)
/Users/buithiphuongthao/.local/bin/vibe-trading alpha bench --zoo alpha101 --top 20

# Khởi chạy MCP Server (nếu cần kết nối qua giao thức MCP)
/Users/buithiphuongthao/.local/bin/vibe-trading-mcp --help
```

---

## 3. Gọi qua Python (`/Users/buithiphuongthao/.hermes/hkuds-vibe-trading/.venv/bin/python`)
Khi viết script Python sử dụng các module nội bộ của `HKUDS/Vibe-Trading` (`src`, `backtest`, `src.factors`, `src.quantlib`), luôn chạy bằng:
```bash
/Users/buithiphuongthao/.hermes/hkuds-vibe-trading/.venv/bin/python <script.py>
```
