from __future__ import annotations
import math
from typing import List


def _base_price(symbol: str) -> float:
    mapping = {"BTCUSDT": 85000.0, "ETHUSDT": 4200.0, "SOLUSDT": 180.0}
    return mapping.get(symbol, 100.0)


def generate_signals(symbols: List[str], timeframe: str) -> list[dict]:
    signals = []
    for i, symbol in enumerate(symbols, start=1):
        base = _base_price(symbol)
        phase = i * 0.7 + len(timeframe)
        prob_up = round(0.5 + 0.18 * math.sin(phase), 3)
        confidence = round(0.55 + 0.2 * abs(math.cos(phase)), 3)
        expected_move = round((prob_up - 0.5) * 0.08, 4)
        action = "buy" if prob_up >= 0.58 else "sell" if prob_up <= 0.42 else "hold"
        signals.append(
            {
                "symbol": symbol,
                "timeframe": timeframe,
                "price": base,
                "prob_up": prob_up,
                "prob_down": round(1 - prob_up, 3),
                "confidence": confidence,
                "expected_move": expected_move,
                "action": action,
            }
        )
    return sorted(signals, key=lambda x: (x["confidence"], abs(x["expected_move"])), reverse=True)
