# Future Engine Final

Arquitetura completa para validar tudo em **paper mode** e só depois ligar o modo real sem precisar desenvolver novas peças.

## O que já está pronto
- FastAPI com endpoints de health, sinais, backtest, autotrade, scheduler e portfolio
- Streamlit com painel de operação
- Toggle visual de **modo real** no painel
- **Modo real desligado por padrão** (`LIVE_TRADING_ENABLED=false`)
- Guardrails para impedir ordem real quando o modo não estiver liberado
- Exchange adapter com `paper`, `live_stub` e `ccxt_binance`
- Scheduler interno para rodar o ciclo completo
- Journal de ordens, eventos e PnL consolidado
- Docker Compose para subir a stack local
- Testes básicos

## Arquitetura

```text
UI (Streamlit)
   |
FastAPI
   |-- Signal Engine
   |-- Risk Engine
   |-- Backtest Engine
   |-- Portfolio Engine
   |-- Scheduler Engine
   |-- Execution Engine
             |-- paper
             |-- live_stub
             |-- ccxt_binance
```

## Modo real
O sistema já está preparado para operação real, mas por segurança ele nasce bloqueado.

Variáveis principais no `.env`:

```env
LIVE_TRADING_ENABLED=false
EXCHANGE_MODE=paper
EXCHANGE_PROVIDER=paper
```

Para liberar depois, basta mudar para algo como:

```env
LIVE_TRADING_ENABLED=true
EXCHANGE_MODE=live
EXCHANGE_PROVIDER=ccxt_binance
BINANCE_API_KEY=...
BINANCE_API_SECRET=...
CCXT_ENABLED=true
```

## Como subir localmente

```bash
cp .env.example .env
docker compose up --build
```

## URLs
- API docs: http://localhost:8000/docs
- UI: http://localhost:8501

## Fluxo recomendado de teste

### Etapa 1 — Subir o projeto
```bash
cp .env.example .env
docker compose up --build
```

### Etapa 2 — Validar saúde
Abrir:
- `GET /health`
- `GET /ops/status`

### Etapa 3 — Gerar sinais
No Swagger ou na UI, rodar `/signals/generate` com algo como:

```json
{
  "symbols": ["BTCUSDT", "ETHUSDT", "SOLUSDT"],
  "timeframe": "4h"
}
```

### Etapa 4 — Rodar backtest
Endpoint `/backtest/run`

```json
{
  "symbol": "BTCUSDT",
  "periods": 180,
  "timeframe": "4h"
}
```

### Etapa 5 — Rodar autotrade em papel
Endpoint `/autotrade/run`

```json
{
  "symbols": ["BTCUSDT", "ETHUSDT", "SOLUSDT"],
  "timeframe": "4h",
  "capital": 1000
}
```

### Etapa 6 — Rodar scheduler
Endpoint `/scheduler/run-cycle`

Isso executa:
1. geração de sinais
2. ranking
3. filtro de risco
4. execução paper/live conforme configuração
5. atualização do portfolio

### Etapa 7 — Acompanhar resultados
- `GET /portfolio/positions`
- `GET /portfolio/pnl`
- `GET /ops/orders`
- `GET /ops/events`

## Como ligar o modo real depois
Quando você terminar os testes em paper:

1. editar `.env`
2. trocar `LIVE_TRADING_ENABLED=true`
3. trocar `EXCHANGE_MODE=live`
4. escolher `EXCHANGE_PROVIDER=ccxt_binance`
5. adicionar credenciais
6. reiniciar `docker compose up --build`

O sistema já tem a trava. Se o modo real estiver desligado, ele bloqueia ordem real automaticamente.

## Observações importantes
- O adapter `ccxt_binance` está preparado, mas nesta entrega ele fica em modo de demonstração se as credenciais não forem fornecidas.
- Não há ordem real sem `LIVE_TRADING_ENABLED=true`.
- O scheduler recorrente em produção deve usar Celery Beat ou cron gerenciado. Nesta entrega ficou um scheduler local/manual simples para teste rápido.

## Estrutura

```text
app/
  api/
  core/
  services/
  models/
ui/
tests/
Dockerfile
docker-compose.yml
requirements.txt
```
