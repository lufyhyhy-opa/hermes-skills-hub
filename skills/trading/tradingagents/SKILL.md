---
name: tradingagents
description: "TauricResearch/TradingAgents (v0.7.1) — Multi-Agent LLM Financial & Crypto Trading Firm Framework. Simulates a full institutional trading desk with parallel Analysts (Technical/Market, Sentiment, News, Fundamentals), Bullish vs Bearish Researchers debate, Trader Agent, Risk Management Team (Conservative, Neutral, Aggressive), and Portfolio Manager. Supports BTC-USD, ETH-USD, SOL-USD, equities, and OpenAI-compatible endpoints."
version: 0.7.1
author: TauricResearch (Integrated for Hermes Agent — Ai trading)
license: Apache-2.0
platforms: [macos, linux, windows]
metadata:
  tags: [tradingagents, multi-agent, tauric, crypto-debate, bull-vs-bear, risk-manager, langgraph, trading-desk]
  hermes:
    tags: [TradingAgents, MultiAgentDebate, BullBearDebate, RiskManagement, CryptoTradingDesk]
    related_skills: [vibetrading, hkuds-vibe-trading, research]
---

# TradingAgents (`TauricResearch/TradingAgents` — Multi-Agent Trading Desk Framework)

- **Repository Root:** `/Users/buithiphuongthao/.hermes/tradingagents`
- **Dedicated Python Venv:** `/Users/buithiphuongthao/.hermes/tradingagents/.venv/bin/python`
- **Global CLI Executable:** `/Users/buithiphuongthao/.local/bin/tradingagents`
- **Default Config Reference:** `/Users/buithiphuongthao/.hermes/tradingagents/tradingagents/default_config.py`

---

## 1. Kiến trúc Hội Đồng Đa Tác Nhân (Multi-Agent Trading Firm)
Khi kích hoạt `tradingagents` cho một mã Crypto (`BTC-USD`, `ETH-USD`, `SOL-USD`, `BNB-USD`...) hoặc cổ phiếu (`NVDA`, `AAPL`...), hệ thống vận hành 4 tầng:
1. **Analyst Team (Chạy song song):**
   - `market` (Technical Analyst): Phân tích kỹ thuật (MACD, RSI, Bollinger Bands, ATR, VWAP...).
   - `sentiment` (Sentiment Analyst): Đo lường tâm lý thị trường trên mạng xã hội (Reddit, StockTwits, Crypto chatter).
   - `news` (News Analyst): Phân tích tin tức vĩ mô và sự kiện thị trường.
   - `fundamentals` (Fundamentals Analyst): Phân tích dữ liệu cơ bản / định giá.
2. **Researcher Team (Tranh biện Đa chiều):**
   - **Bullish Researcher** vs **Bearish Researcher** tranh luận qua nhiều vòng (`max_debate_rounds`) để phản biện luận điểm của nhau, do **Research Manager** tổng hợp.
3. **Trader Agent:**
   - Đề xuất quyết định giao dịch cụ thể (Mua / Bán / Giữ, thời điểm và quy mô vị thế).
4. **Risk Management Team & Portfolio Manager:**
   - 3 chuyên gia rủi ro (**Aggressive / Conservative / Neutral**) tranh biện (`max_risk_rounds`) trước khi **Portfolio Manager** phê duyệt quyết định cuối cùng và lưu báo cáo HTML/Markdown.

---

## 2. Chạy nhanh qua CLI (`tradingagents`)

Để chạy không cần tương tác (headless/script mode) cho Crypto (ví dụ `BTC-USD`, `ETH-USD`, `SOL-USD`):

```bash
export TRADINGAGENTS_LLM_PROVIDER=openai_compatible
export TRADINGAGENTS_LLM_BACKEND_URL="https://api.xingchiapi.com/v1"
export OPENAI_COMPATIBLE_API_KEY="$(grep '^HERMES_CUSTOM_XINGCHI_API_KEY=' ~/.hermes/profiles/ai-trading/.env | cut -d= -f2-)"
export TRADINGAGENTS_QUICK_THINK_LLM="gpt-6.1-sol"
export TRADINGAGENTS_DEEP_THINK_LLM="gpt-6.1-sol"
export TRADINGAGENTS_OUTPUT_LANGUAGE="Vietnamese"
export TRADINGAGENTS_MAX_DEBATE_ROUNDS=1
export TRADINGAGENTS_MAX_RISK_ROUNDS=1
export TRADINGAGENTS_NO_UPDATE_CHECK=1

/Users/buithiphuongthao/.local/bin/tradingagents \
  --ticker BTC-USD \
  --date 2026-11-16 \
  --analysts market,news,sentiment \
  --save --no-show
```

---

## 3. Sử dụng trong Python (`/Users/buithiphuongthao/.hermes/tradingagents/.venv/bin/python`)

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "openai_compatible"
config["backend_url"] = "https://api.xingchiapi.com/v1"
config["deep_think_llm"] = "gpt-6.1-sol"
config["quick_think_llm"] = "gpt-6.1-sol"
config["max_debate_rounds"] = 1
config["max_risk_rounds"] = 1

ta = TradingAgentsGraph(
    selected_analysts=["market", "news", "sentiment"],
    debug=True,
    config=config,
)

state, decision = ta.propagate("BTC-USD", "2026-11-16")
print(decision)
ta.save_reports(state, "BTC-USD")
```

### Truyền danh mục hiện tại (`PortfolioContext`) để quản trị rủi ro sát thực tế:
```python
from tradingagents.portfolio import PortfolioContext

portfolio = PortfolioContext.model_validate({
    "cash": 10000.0,
    "currency": "USD",
    "positions": [{"ticker": "BTC-USD", "quantity": 0.15, "average_price": 85000.0}],
})
state, decision = ta.propagate("BTC-USD", "2026-11-16", portfolio=portfolio)
```
