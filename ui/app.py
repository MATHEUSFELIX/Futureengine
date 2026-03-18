import os
import streamlit as st
import httpx

API = os.getenv("API_URL", "http://api:8000")

st.set_page_config(page_title="Future Engine Final", layout="wide")
st.title("Future Engine Final")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Modo", os.getenv("EXCHANGE_MODE", "paper"))
with col2:
    st.metric("Provider", os.getenv("EXCHANGE_PROVIDER", "paper"))
with col3:
    st.metric("Modo real liberado", os.getenv("LIVE_TRADING_ENABLED", "false"))

st.subheader("Trava do modo real")
live_toggle = st.toggle("Modo real", value=os.getenv("LIVE_TRADING_ENABLED", "false").lower() == "true", disabled=True)
st.caption("O botão já existe no painel, mas fica travado pelo .env. Assim você testa tudo antes e só liga o modo real depois.")

symbols = st.multiselect("Ativos", ["BTCUSDT", "ETHUSDT", "SOLUSDT"], default=["BTCUSDT", "ETHUSDT", "SOLUSDT"])
timeframe = st.selectbox("Timeframe", ["1h", "4h", "1d"], index=1)
capital = st.number_input("Capital", value=1000.0, step=100.0)

client = httpx.Client(timeout=30.0)

c1, c2, c3 = st.columns(3)
if c1.button("Gerar sinais"):
    r = client.post(f"{API}/signals/generate", json={"symbols": symbols, "timeframe": timeframe})
    st.json(r.json())
if c2.button("Rodar backtest"):
    r = client.post(f"{API}/backtest/run", json={"symbol": symbols[0], "periods": 180, "timeframe": timeframe})
    st.json(r.json())
if c3.button("Rodar ciclo completo"):
    r = client.post(f"{API}/scheduler/run-cycle", json={"symbols": symbols, "timeframe": timeframe, "capital": capital})
    st.json(r.json())

st.subheader("Status")
if st.button("Atualizar status"):
    st.json(client.get(f"{API}/ops/status").json())
    st.json(client.get(f"{API}/portfolio/pnl").json())
    st.json(client.get(f"{API}/portfolio/positions").json())
