from pydantic import BaseModel, Field
from typing import List

class SignalRequest(BaseModel):
    symbols: List[str] = Field(default_factory=lambda: ["BTCUSDT", "ETHUSDT", "SOLUSDT"])
    timeframe: str = "4h"

class BacktestRequest(BaseModel):
    symbol: str = "BTCUSDT"
    periods: int = 180
    timeframe: str = "4h"

class AutoTradeRequest(BaseModel):
    symbols: List[str] = Field(default_factory=lambda: ["BTCUSDT", "ETHUSDT", "SOLUSDT"])
    timeframe: str = "4h"
    capital: float = 1000

class Order(BaseModel):
    symbol: str
    side: str
    quantity: float
    mode: str
    status: str
    price: float
    reason: str
