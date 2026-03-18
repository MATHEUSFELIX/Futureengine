from __future__ import annotations
from app.core.config import settings


def execute_order(symbol: str, side: str, quantity: float, price: float, reason: str) -> dict:
    mode = settings.exchange_mode
    provider = settings.exchange_provider

    if mode == "live" and not settings.live_trading_enabled:
        return {
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "mode": mode,
            "status": "blocked",
            "price": price,
            "reason": "LIVE_TRADING_ENABLED=false",
            "provider": provider,
        }

    if provider == "ccxt_binance":
        if not settings.ccxt_enabled or not settings.binance_api_key or not settings.binance_api_secret:
            return {
                "symbol": symbol,
                "side": side,
                "quantity": quantity,
                "mode": mode,
                "status": "simulated",
                "price": price,
                "reason": "ccxt provider configured without full live credentials",
                "provider": provider,
            }

    return {
        "symbol": symbol,
        "side": side,
        "quantity": quantity,
        "mode": mode,
        "status": "executed" if mode == "paper" else "submitted",
        "price": price,
        "reason": reason,
        "provider": provider,
    }
