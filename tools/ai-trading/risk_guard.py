#!/Users/buithiphuongthao/.hermes/vibetrading/.venv/bin/python
"""
Risk Guard — Hard-Coded Risk Management, Position Sizing & Emergency Circuit Breaker
Equipped for Hermes Agent: Ai trading (ai-trading)
"""

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

STATE_FILE = Path("/Users/buithiphuongthao/.hermes/profiles/ai-trading/workspace/risk_guard_state.json")

DEFAULT_LIMITS = {
    "kill_switch": False,
    "kill_reason": "",
    "max_risk_per_trade_pct": 2.0,
    "max_daily_drawdown_pct": 4.0,
    "max_leverage": 5.0,
    "min_rr_ratio": 1.5,
    "daily_realized_loss_pct": 0.0,
    "updated_at": "",
}


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            data = json.loads(STATE_FILE.read_text())
            return {**DEFAULT_LIMITS, **data}
        except Exception:
            pass
    return DEFAULT_LIMITS.copy()


def save_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False))


def calculate_position(
    balance: float,
    risk_pct: float,
    entry: float,
    stop_loss: float,
    take_profit: float,
    leverage: float = 1.0,
) -> dict:
    state = load_state()
    effective_risk_pct = min(risk_pct, state["max_risk_per_trade_pct"])
    risk_usd = balance * (effective_risk_pct / 100.0)
    stop_dist = abs(entry - stop_loss)
    if stop_dist <= 0:
        return {"valid": False, "error": "Entry and Stop-Loss cannot be identical."}

    side = "LONG" if entry > stop_loss else "SHORT"
    reward_dist = (take_profit - entry) if side == "LONG" else (entry - take_profit)
    rr_ratio = reward_dist / stop_dist if stop_dist > 0 else 0.0

    qty = risk_usd / stop_dist
    notional_usd = qty * entry
    margin_required = notional_usd / max(leverage, 1.0)
    effective_account_leverage = notional_usd / balance if balance > 0 else 0.0

    violations = []
    if state["kill_switch"]:
        violations.append(f"KILL_SWITCH_ACTIVE: {state.get('kill_reason') or 'Manual halt'}")
    if state["daily_realized_loss_pct"] >= state["max_daily_drawdown_pct"]:
        violations.append(
            f"DAILY_DRAWDOWN_BREACHED: {state['daily_realized_loss_pct']}% >= {state['max_daily_drawdown_pct']}%"
        )
    if risk_pct > state["max_risk_per_trade_pct"]:
        violations.append(
            f"RISK_CAPPED: Requested {risk_pct}% exceeds max_risk_per_trade_pct ({state['max_risk_per_trade_pct']}%). Auto-capped to {effective_risk_pct}%."
        )
    if leverage > state["max_leverage"]:
        violations.append(
            f"LEVERAGE_EXCEEDED: {leverage}x > max allowed {state['max_leverage']}x"
        )
    if rr_ratio < state["min_rr_ratio"]:
        violations.append(
            f"LOW_RR_RATIO: R:R is {rr_ratio:.2f} (< minimum {state['min_rr_ratio']})"
        )
    if margin_required > balance:
        violations.append(
            f"INSUFFICIENT_MARGIN: Required margin ${margin_required:,.2f} exceeds balance ${balance:,.2f}"
        )

    approved = not any(
        v.startswith(("KILL_SWITCH", "DAILY_DRAWDOWN", "LEVERAGE_EXCEEDED", "LOW_RR_RATIO", "INSUFFICIENT_MARGIN"))
        for v in violations
    )

    return {
        "approved": approved,
        "side": side,
        "balance_usd": round(balance, 2),
        "risk_pct_applied": round(effective_risk_pct, 2),
        "max_loss_usd": round(risk_usd, 2),
        "expected_profit_usd": round(qty * reward_dist, 2),
        "rr_ratio": round(rr_ratio, 2),
        "entry": entry,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "recommended_qty": round(qty, 6),
        "notional_value_usd": round(notional_usd, 2),
        "leverage": leverage,
        "margin_required_usd": round(margin_required, 2),
        "effective_account_leverage": round(effective_account_leverage, 2),
        "violations": violations,
    }


def main():
    parser = argparse.ArgumentParser(description="Risk Guard — Hard Risk Rules & Kill Switch")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_size = sub.add_parser("size", help="Calculate safe position size & check risk guardrails")
    p_size.add_argument("--balance", type=float, required=True, help="Account balance in USD")
    p_size.add_argument("--risk-pct", type=float, default=1.0, help="Risk per trade % (default 1.0)")
    p_size.add_argument("--entry", type=float, required=True, help="Entry price")
    p_size.add_argument("--sl", type=float, required=True, help="Stop-loss price")
    p_size.add_argument("--tp", type=float, required=True, help="Take-profit price")
    p_size.add_argument("--leverage", type=float, default=3.0, help="Leverage (default 3x)")

    p_kill = sub.add_parser("kill-switch", help="Manage emergency kill switch")
    p_kill.add_argument("--on", action="store_true", help="Activate kill switch")
    p_kill.add_argument("--off", action="store_true", help="Deactivate kill switch & reset daily loss")
    p_kill.add_argument("--reason", default="Triggered by user or daily drawdown limit", help="Reason")

    sub.add_parser("status", help="Show current risk limits and circuit breaker status")

    args = parser.parse_args()
    if args.cmd == "size":
        res = calculate_position(
            balance=args.balance,
            risk_pct=args.risk_pct,
            entry=args.entry,
            stop_loss=args.sl,
            take_profit=args.tp,
            leverage=args.leverage,
        )
        print(json.dumps(res, indent=2, ensure_ascii=False))
    elif args.cmd == "kill-switch":
        st = load_state()
        if args.on:
            st["kill_switch"] = True
            st["kill_reason"] = args.reason
        elif args.off:
            st["kill_switch"] = False
            st["kill_reason"] = ""
            st["daily_realized_loss_pct"] = 0.0
        save_state(st)
        print(json.dumps(st, indent=2, ensure_ascii=False))
    elif args.cmd == "status":
        print(json.dumps(load_state(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
