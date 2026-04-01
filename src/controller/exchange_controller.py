from fastapi import APIRouter
from fastapi.responses import JSONResponse
from httpx import Response
from datetime import datetime
import httpx

from src.model.external.exchange_api_types import ExchangeApiSuccess, ExchangeValue
from src.model.exchange_controller_types import ExchangeResponse, Currency
from src.model.env_settings import EnvSettings

env = EnvSettings()
router = APIRouter()


@router.get("/exchange/{currency}/{original}")
async def calculate_exchange(currency: Currency, original: float) -> JSONResponse:
    client = httpx.AsyncClient(verify=False)
    response: Response = await client.get(
        f"{env.exchange_api_url}/{currency.value}/{datetime.now()}"
    )
    parsed_response: ExchangeApiSuccess

    try:
        response.raise_for_status()
    except Exception:
        return JSONResponse(status_code=response.status_code, content=response.json())

    parsed_response = ExchangeApiSuccess(**response.json())
    rate: ExchangeValue = max(
        parsed_response.cotacoes, key=lambda c: c.data_hora_cotacao
    )

    if not rate:
        raise RuntimeError("API Response returned empty")

    exchange_response = ExchangeResponse(
        bid_rate=rate.cotacao_compra,
        ask_rate=rate.cotacao_venda,
        rate_date=rate.data_hora_cotacao,
        bid=original / rate.cotacao_compra / rate.paridade_compra,
        ask=original / rate.cotacao_venda / rate.paridade_venda,
        currency=parsed_response.moeda,
    )
    return JSONResponse(
        status_code=200, content=exchange_response.model_dump(mode="json")
    )
