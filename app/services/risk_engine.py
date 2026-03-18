from __future__ import annotations
from app.core.config import settings


def approve_signal(signal: dict) -> dict:
    allowed = signal["action"] != "hold" and signal["confidence"] >= 0.62 and abs(signal["expected_move"]) >= 0.004
    qty_fraction = settings.risk_per_trade if allowed else 0.0
    return {
        **signal,
        "risk_allowed": allowed,
        "risk_reason": "approved" if allowed else "blocked_by_thresholds",
        "qty_fraction": qty_fraction,
    }
