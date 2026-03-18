from __future__ import annotations
from app.services.signal_engine import generate_signals
from app.services.risk_engine import approve_signal
from app.services.execution_engine import execute_order
from app.services.portfolio_engine import update_position
from app.services.store import STORE


def run_cycle(symbols: list[str], timeframe: str, capital: float) -> dict:
    signals = generate_signals(symbols, timeframe)
    approved = [approve_signal(s) for s in signals]
    orders = []
    for signal in approved:
        if not signal["risk_allowed"]:
            continue
        notional = capital * signal["qty_fraction"]
        quantity = round(notional / signal["price"], 6)
        order = execute_order(
            symbol=signal["symbol"],
            side=signal["action"],
            quantity=quantity,
            price=signal["price"],
            reason=f"prob_up={signal['prob_up']} confidence={signal['confidence']}",
        )
        STORE["orders"].append(order)
        STORE["events"].append({"type": "order", "symbol": signal["symbol"], "status": order["status"]})
        update_position(order)
        orders.append(order)
    STORE["signals"] = approved
    return {"signals": approved, "orders": orders, "executed": len(orders)}
