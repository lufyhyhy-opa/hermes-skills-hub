---
name: crypto-radar
description: "Real-Time Crypto Market Intelligence, Multi-Timeframe Technical Scanner (15m/1h/4h/1d RSI, EMA20/50, ATR), Orderbook Imbalance, Hyperliquid Top Open Interest & Funding Rate Radar, and Crypto Fear & Greed Index. Use before making any trading decision to get live prices, derivatives sentiment, and multi-timeframe trend alignment."
version: 1.0.0
author: Integrated for Hermes Agent — Ai trading
license: MIT
platforms: [macos, linux, windows]
metadata:
  tags: [crypto-radar, hyperliquid, funding-rate, open-interest, fear-and-greed, orderbook, multi-timeframe]
  hermes:
    tags: [CryptoRadar, HyperliquidOI, FundingRate, OrderbookImbalance, FearAndGreed]
    related_skills: [vibetrading, hkuds-vibe-trading, tradingagents, risk-guard, trade-journal]
---

# Crypto Radar (`crypto-radar` — Real-Time Market, Derivatives & Hyperliquid Scanner)

- **Executable CLI:** `/Users/buithiphuongthao/.local/bin/crypto-radar`
- **Source Script:** `/Users/buithiphuongthao/.hermes/profiles/ai-trading/tools/crypto_radar.py`

## Các Lệnh Chạy Trực Tiếp (Không Cần API Key)

```bash
# 1. Quét toàn cảnh thị trường (Fear & Greed + Top 10 OI/Funding trên Hyperliquid + Đa khung 15m/1h/4h/1d cho BTC, ETH, SOL)
/Users/buithiphuongthao/.local/bin/crypto-radar overview

# 2. Quét kỹ thuật đa khung (15m, 1h, 4h, 1d) + Tường lệnh Orderbook (Bid/Ask Imbalance) cho bất kỳ cặp coin nào
/Users/buithiphuongthao/.local/bin/crypto-radar scan --symbols "BTC/USDT,ETH/USDT,SOL/USDT,SUI/USDT"

# 3. Xem Top Open Interest (OI), Funding Rate & Volume 24h trực tiếp trên sàn Hyperliquid
/Users/buithiphuongthao/.local/bin/crypto-radar hyperliquid --top 15

# 4. Kiểm tra chỉ số Fear & Greed Index hôm nay so với hôm qua
/Users/buithiphuongthao/.local/bin/crypto-radar sentiment
```
