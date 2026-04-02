from fastapi import APIRouter
from fastapi.responses import JSONResponse
from httpx import HTTPStatusError

from src.model.cep_types import Address, Cep
from src.model.env_settings import EnvSettings
from src.service.cep_requests import request_address
from src.infrastructure.logger import logger

env = EnvSettings()
router = APIRouter()


@router.get("/cep/{cep}")
async def get_cep(cep: Cep) -> JSONResponse:
    status_code: int
    content: dict
    try:
        address: Address = await request_address(cep)
        status_code = 200
        content = address.model_dump()
    except HTTPStatusError as e:
        logger.error("External CEP API returned an error")
        status_code = e.response.status_code
        content = e.response.json()
    return JSONResponse(status_code=status_code, content=content)
