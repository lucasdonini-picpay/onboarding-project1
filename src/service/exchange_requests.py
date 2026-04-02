from src.model.exchange_types import Currency, ExchangeResponse
from src.model.external.exchange_api_types import ExchangeApiSuccess
from src.model.env_settings import EnvSettings
from datetime import datetime
import httpx

env = EnvSettings()
client = httpx.AsyncClient(verify=False)


async def calculate_exchange(currency: Currency, original: float) -> ExchangeResponse:
    response = await client.get(
        f"{env.exchange_api_url}/{currency.value}/{datetime.now()}"
    )
    response.raise_for_status()
    success = ExchangeApiSuccess(**response.json())
    rate = max(success.cotacoes, key=lambda c: c.data_hora_cotacao)
    return ExchangeResponse(
        bid_rate=rate.cotacao_compra,
        ask_rate=rate.cotacao_venda,
        rate_date=rate.data_hora_cotacao,
        bid=original / rate.cotacao_compra / rate.paridade_compra,
        ask=original / rate.cotacao_venda / rate.paridade_venda,
        currency=success.moeda,
    )
