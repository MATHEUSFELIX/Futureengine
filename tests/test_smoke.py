from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_signal_and_backtest():
    r1 = client.post("/signals/generate", json={"symbols": ["BTCUSDT"], "timeframe": "4h"})
    assert r1.status_code == 200
    assert len(r1.json()["signals"]) == 1

    r2 = client.post("/backtest/run", json={"symbol": "BTCUSDT", "periods": 180, "timeframe": "4h"})
    assert r2.status_code == 200
    assert "expectancy" in r2.json()
