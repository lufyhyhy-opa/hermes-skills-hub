#!/Users/buithiphuongthao/.hermes/vibetrading/.venv/bin/python
"""
Trade Journal & Post-Mortem Memory — SQLite Ledger & Live Signal Evaluator
Equipped for Hermes Agent: Ai trading (ai-trading)
"""

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
import ccxt

DB_PATH = Path("/Users/buithiphuongthao/.hermes/profiles/ai-trading/workspace/trade_journal.db")


def get_conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            symbol TEXT NOT NULL,
            side TEXT NOT NULL,
            entry_price REAL NOT NULL,
            stop_loss REAL NOT NULL,
            take_profit REAL NOT NULL,
            qty REAL DEFAULT 0.0,
            leverage REAL DEFAULT 1.0,
            strategy_source TEXT DEFAULT '',
            thesis TEXT DEFAULT '',
            status TEXT DEFAULT 'OPEN',
            exit_price REAL,
            pnl_pct REAL,
            closed_at TEXT,
            lesson_learned TEXT DEFAULT ''
        )
        """
    )
    conn.commit()
    return conn


def log_trade(args) -> dict:
    conn = get_conn()
    now = datetime.now(timezone.utc).isoformat()
    cur = conn.execute(
        """
        INSERT INTO trades (created_at, symbol, side, entry_price, stop_loss, take_profit, qty, leverage, strategy_source, thesis, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'OPEN')
        """,
        (
            now,
            args.symbol.upper(),
            args.side.upper(),
            args.entry,
            args.sl,
            args.tp,
            args.qty,
            args.leverage,
            args.source,
            args.thesis,
        ),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM trades WHERE id = ?", (cur.lastrowid,)).fetchone()
    return dict(row)


def evaluate_open_trades(exchange_id: str = "binance") -> list[dict]:
    conn = get_conn()
    rows = conn.execute("SELECT * FROM trades WHERE status = 'OPEN' ORDER BY id DESC").fetchall()
    if not rows:
        return []

    ex = getattr(ccxt, exchange_id)({"enableRateLimit": True})
    results = []
    for r in rows:
        d = dict(r)
        sym = d["symbol"]
        if "/" not in sym:
            sym = f"{sym}/USDT"
        try:
            ticker = ex.fetch_ticker(sym)
            curr_price = float(ticker["last"])
            entry = float(d["entry_price"])
            sl = float(d["stop_loss"])
            tp = float(d["take_profit"])
            lev = float(d["leverage"] or 1.0)
            is_long = d["side"].upper() == "LONG"

            raw_move = ((curr_price - entry) / entry) if is_long else ((entry - curr_price) / entry)
            pnl_pct = raw_move * lev * 100.0

            hit = "IN_PROGRESS"
            if is_long:
                if curr_price >= tp:
                    hit = "HIT_TP"
                elif curr_price <= sl:
                    hit = "HIT_SL"
            else:
                if curr_price <= tp:
                    hit = "HIT_TP"
                elif curr_price >= sl:
                    hit = "HIT_SL"

            d["current_price"] = curr_price
            d["unrealized_pnl_pct"] = round(pnl_pct, 2)
            d["evaluation"] = hit
        except Exception as e:
            d["evaluation_error"] = str(e)
        results.append(d)
    return results


def close_trade(trade_id: int, exit_price: float, lesson: str) -> dict:
    conn = get_conn()
    row = conn.execute("SELECT * FROM trades WHERE id = ?", (trade_id,)).fetchone()
    if not row:
        return {"error": f"Trade ID {trade_id} not found"}
    d = dict(row)
    entry = float(d["entry_price"])
    lev = float(d["leverage"] or 1.0)
    is_long = d["side"].upper() == "LONG"
    raw_move = ((exit_price - entry) / entry) if is_long else ((entry - exit_price) / entry)
    pnl_pct = round(raw_move * lev * 100.0, 2)
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        """
        UPDATE trades
        SET status = 'CLOSED', exit_price = ?, pnl_pct = ?, closed_at = ?, lesson_learned = ?
        WHERE id = ?
        """,
        (exit_price, pnl_pct, now, lesson, trade_id),
    )
    conn.commit()
    return dict(conn.execute("SELECT * FROM trades WHERE id = ?", (trade_id,)).fetchone())


def get_stats() -> dict:
    conn = get_conn()
    all_rows = [dict(r) for r in conn.execute("SELECT * FROM trades ORDER BY id DESC").fetchall()]
    closed = [r for r in all_rows if r["status"] == "CLOSED" and r["pnl_pct"] is not None]
    open_trades = [r for r in all_rows if r["status"] == "OPEN"]
    wins = [r for r in closed if r["pnl_pct"] > 0]
    losses = [r for r in closed if r["pnl_pct"] <= 0]
    win_rate = (len(wins) / len(closed) * 100.0) if closed else 0.0
    avg_pnl = (sum(r["pnl_pct"] for r in closed) / len(closed)) if closed else 0.0
    return {
        "total_logged": len(all_rows),
        "open_trades": len(open_trades),
        "closed_trades": len(closed),
        "win_rate_pct": round(win_rate, 2),
        "avg_pnl_pct": round(avg_pnl, 2),
        "recent_lessons": [
            {"id": r["id"], "symbol": r["symbol"], "pnl_pct": r["pnl_pct"], "lesson": r["lesson_learned"]}
            for r in closed[:10]
            if r.get("lesson_learned")
        ],
        "recent_trades": all_rows[:10],
    }


def main():
    parser = argparse.ArgumentParser(description="Trade Journal & Post-Mortem Memory")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_log = sub.add_parser("log", help="Log a new trade signal or position")
    p_log.add_argument("--symbol", required=True, help="e.g. BTC/USDT")
    p_log.add_argument("--side", required=True, choices=["LONG", "SHORT", "long", "short"])
    p_log.add_argument("--entry", type=float, required=True)
    p_log.add_argument("--sl", type=float, required=True)
    p_log.add_argument("--tp", type=float, required=True)
    p_log.add_argument("--qty", type=float, default=0.0)
    p_log.add_argument("--leverage", type=float, default=3.0)
    p_log.add_argument("--source", default="Ai trading")
    p_log.add_argument("--thesis", default="")

    sub.add_parser("evaluate", help="Evaluate all OPEN trades against live market prices")

    p_close = sub.add_parser("close", help="Close a trade and record post-mortem lesson")
    p_close.add_argument("--id", type=int, required=True)
    p_close.add_argument("--exit-price", type=float, required=True)
    p_close.add_argument("--lesson", default="")

    sub.add_parser("stats", help="Show trade journal statistics and post-mortem lessons")

    args = parser.parse_args()
    if args.cmd == "log":
        print(json.dumps(log_trade(args), indent=2, ensure_ascii=False))
    elif args.cmd == "evaluate":
        print(json.dumps(evaluate_open_trades(), indent=2, ensure_ascii=False))
    elif args.cmd == "close":
        print(json.dumps(close_trade(args.id, args.exit_price, args.lesson), indent=2, ensure_ascii=False))
    elif args.cmd == "stats":
        print(json.dumps(get_stats(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
