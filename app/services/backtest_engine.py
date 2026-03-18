from __future__ import annotations


def run_backtest(symbol: str, periods: int, timeframe: str) -> dict:
    win_rate = round(min(0.72, 0.51 + periods / 1000), 3)
    gain = 0.018
    loss = 0.011
    expectancy = round(win_rate * gain - (1 - win_rate) * loss, 4)
    max_drawdown = round(min(0.2, 0.04 + periods / 5000), 3)
    sharpe_like = round((expectancy / max(max_drawdown, 0.01)) * 5, 3)
    return {
        "symbol": symbol,
        "timeframe": timeframe,
        "periods": periods,
        "win_rate": win_rate,
        "avg_gain": gain,
        "avg_loss": loss,
        "expectancy": expectancy,
        "max_drawdown": max_drawdown,
        "sharpe_like": sharpe_like,
    }
