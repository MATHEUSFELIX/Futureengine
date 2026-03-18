from __future__ import annotations
from app.services.store import STORE


def update_position(order: dict) -> None:
    if order["status"] not in {"executed", "submitted", "simulated"}:
        return
    sym = order["symbol"]
    current = STORE["positions"].get(sym, {"symbol": sym, "net_qty": 0.0, "avg_price": 0.0})
    signed_qty = order["quantity"] if order["side"] == "buy" else -order["quantity"]
    new_qty = current["net_qty"] + signed_qty
    current["avg_price"] = order["price"]
    current["net_qty"] = round(new_qty, 6)
    STORE["positions"][sym] = current


def get_positions() -> list[dict]:
    return list(STORE["positions"].values())


def get_pnl() -> dict:
    unrealized = 0.0
    exposure = 0.0
    for pos in STORE["positions"].values():
        exposure += abs(pos["net_qty"] * pos["avg_price"])
        unrealized += pos["net_qty"] * pos["avg_price"] * 0.01
    return {
        "positions": len(STORE["positions"]),
        "gross_exposure": round(exposure, 2),
        "unrealized_pnl": round(unrealized, 2),
    }
