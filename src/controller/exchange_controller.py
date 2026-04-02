from fastapi import APIRouter
from fastapi.responses import JSONResponse
from httpx import HTTPStatusError

from src.model.exchange_types import Currency, ExchangeResponse
from src.model.env_settings import EnvSettings
from src.service.exchange_requests import calculate_exchange
from src.infrastructure.logger import logger

env = EnvSettings()
router = APIRouter()


@router.get("/exchange/{currency}/{original}")
async def get_exchange(currency: Currency, original: float) -> JSONResponse:
    status_code: int
    content: dict
    try:
        exchange: ExchangeResponse = await calculate_exchange(
            currency=currency, original=original
        )
        status_code = 200
        content = exchange.model_dump(mode="json")
    except HTTPStatusError as e:
        logger.error("External Exchange API returned an error")
        status_code = e.response.status_code
        content = e.response.json()
    return JSONResponse(status_code=status_code, content=content)
