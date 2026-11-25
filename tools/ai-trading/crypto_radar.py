#!/Users/buithiphuongthao/.hermes/vibetrading/.venv/bin/python
"""
Crypto Radar — Real-Time Crypto Intelligence, Derivatives & Hyperliquid Snapshot
Equipped for Hermes Agent: Ai trading (ai-trading)
"""

import argparse
import json
import sys
from datetime import datetime, timezone
import requests
import ccxt
import pandas as pd


def compute_rsi(series: pd.Series, period: int = 14) -> float:
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(window=period).mean()
    loss = (-delta.clip(upper=0)).rolling(window=period).mean()
    rs = gain / loss.replace(0, 1e-10)
    rsi = 100 - (100 / (1 + rs))
    return float(rsi.iloc[-1]) if not rsi.empty else 50.0


def fetch_fear_greed() -> dict:
    try:
        r = requests.get("https://api.alternative.me/fng/?limit=2", timeout=8)
        data = r.json().get("data", [])
        if data:
            curr = data[0]
            prev = data[1] if len(data) > 1 else curr
            return {
                "value": int(curr["value"]),
                "classification": curr["value_classification"],
                "previous_value": int(prev["value"]),
                "previous_classification": prev["value_classification"],
            }
    except Exception as e:
        return {"error": str(e)}
    return {}


def fetch_hyperliquid_top(limit: int = 10) -> list[dict]:
    try:
        r = requests.post(
            "https://api.hyperliquid.xyz/info",
            json={"type": "metaAndAssetCtxs"},
            timeout=10,
        )
        universe, ctxs = r.json()
        assets = universe.get("universe", [])
        rows = []
        for meta, ctx in zip(assets, ctxs):
            mark_px = float(ctx.get("markPx") or 0)
            oi_coins = float(ctx.get("openInterest") or 0)
            oi_usd = oi_coins * mark_px
            funding = float(ctx.get("funding") or 0) * 100  # hourly %
            day_vol = float(ctx.get("dayNtlVlm") or 0)
            prev_px = float(ctx.get("prevDayPx") or mark_px)
            chg_pct = ((mark_px - prev_px) / prev_px * 100) if prev_px > 0 else 0.0
            rows.append(
                {
                    "coin": meta.get("name"),
                    "mark_price": mark_px,
                    "change_24h_pct": round(chg_pct, 2),
                    "funding_hourly_pct": round(funding, 5),
                    "funding_annualized_pct": round(funding * 24 * 365, 2),
                    "open_interest_usd": round(oi_usd, 0),
                    "volume_24h_usd": round(day_vol, 0),
                }
            )
        rows.sort(key=lambda x: x["open_interest_usd"], reverse=True)
        return rows[:limit]
    except Exception as e:
        return [{"error": str(e)}]


def analyze_symbol(symbol: str = "BTC/USDT", exchange_id: str = "binance") -> dict:
    ex_cls = getattr(ccxt, exchange_id)
    ex = ex_cls({"enableRateLimit": True})
    result = {"symbol": symbol, "exchange": exchange_id, "timeframes": {}}

    for tf in ["15m", "1h", "4h", "1d"]:
        try:
            ohlcv = ex.fetch_ohlcv(symbol, timeframe=tf, limit=100)
            df = pd.DataFrame(
                ohlcv, columns=["ts", "open", "high", "low", "close", "volume"]
            )
            close = df["close"]
            high = df["high"]
            low = df["low"]
            ema20 = float(close.ewm(span=20).mean().iloc[-1])
            ema50 = float(close.ewm(span=50).mean().iloc[-1])
            rsi14 = compute_rsi(close, 14)
            tr = pd.concat(
                [
                    high - low,
                    (high - close.shift()).abs(),
                    (low - close.shift()).abs(),
                ],
                axis=1,
            ).max(axis=1)
            atr14 = float(tr.rolling(14).mean().iloc[-1])
            price = float(close.iloc[-1])
            trend = (
                "BULLISH"
                if price > ema20 > ema50
                else ("BEARISH" if price < ema20 < ema50 else "NEUTRAL/CONSOLIDATING")
            )
            result["timeframes"][tf] = {
                "price": round(price, 4),
                "rsi_14": round(rsi14, 2),
                "ema_20": round(ema20, 4),
                "ema_50": round(ema50, 4),
                "atr_14": round(atr14, 4),
                "atr_pct": round(atr14 / price * 100, 2) if price else 0,
                "trend": trend,
            }
        except Exception as e:
            result["timeframes"][tf] = {"error": str(e)}

    # Orderbook Imbalance
    try:
        ob = ex.fetch_order_book(symbol, limit=20)
        bid_vol = sum(b[1] * b[0] for b in ob["bids"][:20])
        ask_vol = sum(a[1] * a[0] for a in ob["asks"][:20])
        total = bid_vol + ask_vol
        imbalance = ((bid_vol - ask_vol) / total * 100) if total > 0 else 0.0
        result["orderbook_top20"] = {
            "bid_wall_usd": round(bid_vol, 2),
            "ask_wall_usd": round(ask_vol, 2),
            "imbalance_pct": round(imbalance, 2),
            "pressure": "BUY_PRESSURE" if imbalance > 10 else ("SELL_PRESSURE" if imbalance < -10 else "BALANCED"),
        }
    except Exception as e:
        result["orderbook_top20"] = {"error": str(e)}

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Crypto Radar — Real-Time Market, Derivatives, Multi-TF & Hyperliquid Scanner"
    )
    parser.add_argument(
        "action",
        choices=["overview", "scan", "hyperliquid", "sentiment"],
        help="Action to run",
    )
    parser.add_argument(
        "--symbols",
        default="BTC/USDT,ETH/USDT,SOL/USDT",
        help="Comma-separated symbols for scan (default: BTC/USDT,ETH/USDT,SOL/USDT)",
    )
    parser.add_argument("--exchange", default="binance", help="CCXT exchange ID")
    parser.add_argument("--top", type=int, default=10, help="Top N markets for hyperliquid")
    args = parser.parse_args()

    out = {"timestamp_utc": datetime.now(timezone.utc).isoformat()}

    if args.action == "sentiment":
        out["fear_and_greed"] = fetch_fear_greed()
    elif args.action == "hyperliquid":
        out["hyperliquid_top_oi"] = fetch_hyperliquid_top(args.top)
    elif args.action == "scan":
        syms = [s.strip() for s in args.symbols.split(",") if s.strip()]
        out["scans"] = [analyze_symbol(s, args.exchange) for s in syms]
    elif args.action == "overview":
        out["fear_and_greed"] = fetch_fear_greed()
        out["hyperliquid_top_oi"] = fetch_hyperliquid_top(args.top)
        syms = [s.strip() for s in args.symbols.split(",") if s.strip()]
        out["scans"] = [analyze_symbol(s, args.exchange) for s in syms]

    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
