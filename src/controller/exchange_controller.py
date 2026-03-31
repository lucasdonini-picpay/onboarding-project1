from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv
from httpx import Response
from datetime import datetime
import httpx, os

from src.model.external.exchange_api_types import ExchangeApiSuccess, ExchangeValue
from src.model.exchange_controller_types import ExchangeRequest, ExchangeResponse

load_dotenv()
ENV_VAR_NAME = "EXCHANGE_API_URL"
BASE_URL = os.getenv(ENV_VAR_NAME)
if not BASE_URL:
    raise RuntimeError(f"Missing environment variable: {ENV_VAR_NAME}")

router = APIRouter()


@router.get("/exchange/{currency}/{original}")
async def calculate_exchange(currency: str, original: float) -> JSONResponse:
    client = httpx.AsyncClient(verify=False)
    response: Response = await client.get(f"{BASE_URL}/{currency}/{datetime.now()}")
    parsed_response: ExchangeApiSuccess

    try:
        response.raise_for_status()
    except Exception:
        return JSONResponse(status_code=response.status_code, content=response.json())

    parsed_response = ExchangeApiSuccess(**response.json())
    rate: ExchangeValue = sorted(
        parsed_response.cotacoes, key=lambda c: c.data_hora_cotacao, reverse=True
    )[0]

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
    return JSONResponse(status_code=200, content=jsonable_encoder(exchange_response))
