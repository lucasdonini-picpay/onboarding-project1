from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from httpx import Response
import httpx

from src.model.external.cep_api_types import CepApiSuccess
from src.model.address import Address
from src.model.env_settings import EnvSettings
from src.utils.cep_utils import validate_cep

env = EnvSettings()
router = APIRouter()


@router.get("/cep/{cep}")
async def get_cep(cep: str) -> JSONResponse:
    if not validate_cep(cep):
        raise ValueError("Invalid CEP")

    client = httpx.AsyncClient(verify=False)
    response: Response = await client.get(f"{env.cep_api_url}/{cep}")

    try:
        response.raise_for_status()
    except Exception:
        return JSONResponse(status_code=response.status_code, content=response.json())

    parsed_response = CepApiSuccess(**response.json())
    address = Address.from_response(parsed_response)
    return JSONResponse(status_code=200, content=jsonable_encoder(address))
