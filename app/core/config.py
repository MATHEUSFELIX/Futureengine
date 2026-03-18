from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    app_env: str = os.getenv("APP_ENV", "dev")
    live_trading_enabled: bool = os.getenv("LIVE_TRADING_ENABLED", "false").lower() == "true"
    exchange_mode: str = os.getenv("EXCHANGE_MODE", "paper")
    exchange_provider: str = os.getenv("EXCHANGE_PROVIDER", "paper")
    ccxt_enabled: bool = os.getenv("CCXT_ENABLED", "false").lower() == "true"
    binance_api_key: str = os.getenv("BINANCE_API_KEY", "")
    binance_api_secret: str = os.getenv("BINANCE_API_SECRET", "")
    scheduler_enabled: bool = os.getenv("SCHEDULER_ENABLED", "false").lower() == "true"
    default_capital: float = float(os.getenv("DEFAULT_CAPITAL", "1000"))
    risk_per_trade: float = float(os.getenv("RISK_PER_TRADE", "0.01"))
    max_daily_loss: float = float(os.getenv("MAX_DAILY_LOSS", "0.03"))

settings = Settings()
