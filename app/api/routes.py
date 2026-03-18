from fastapi import APIRouter
from app.core.config import settings
from app.models.schemas import SignalRequest, BacktestRequest, AutoTradeRequest
from app.services.signal_engine import generate_signals
from app.services.backtest_engine import run_backtest
from app.services.scheduler_engine import run_cycle
from app.services.store import STORE
from app.services.portfolio_engine import get_positions, get_pnl

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok", "env": settings.app_env}

@router.get("/ops/status")
def ops_status():
    return {
        "live_trading_enabled": settings.live_trading_enabled,
        "exchange_mode": settings.exchange_mode,
        "exchange_provider": settings.exchange_provider,
        "ccxt_enabled": settings.ccxt_enabled,
        "signals": len(STORE['signals']),
        "orders": len(STORE['orders']),
    }

@router.post("/signals/generate")
def signals_generate(req: SignalRequest):
    signals = generate_signals(req.symbols, req.timeframe)
    STORE["signals"] = signals
    return {"signals": signals}

@router.post("/backtest/run")
def backtest_run(req: BacktestRequest):
    return run_backtest(req.symbol, req.periods, req.timeframe)

@router.post("/autotrade/run")
def autotrade_run(req: AutoTradeRequest):
    return run_cycle(req.symbols, req.timeframe, req.capital)

@router.post("/scheduler/run-cycle")
def scheduler_run(req: AutoTradeRequest):
    return run_cycle(req.symbols, req.timeframe, req.capital)

@router.get("/portfolio/positions")
def portfolio_positions():
    return {"positions": get_positions()}

@router.get("/portfolio/pnl")
def portfolio_pnl():
    return get_pnl()

@router.get("/ops/orders")
def ops_orders():
    return {"orders": STORE["orders"]}

@router.get("/ops/events")
def ops_events():
    return {"events": STORE["events"]}
