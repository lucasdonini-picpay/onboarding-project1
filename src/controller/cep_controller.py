from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv
from httpx import Response
import httpx, os

from src.model.external.cep_api_types import CepApiSuccess
from src.model.address import Address
from src.utils.cep_utils import validate_cep

load_dotenv()
ENV_VAR_NAME = "CEP_API_URL"
BASE_URL = os.getenv(ENV_VAR_NAME)
if not BASE_URL:
    raise RuntimeError(f"Missing environment variable: {ENV_VAR_NAME}")

router = APIRouter()


@router.get("/cep/{cep}")
async def get_cep(cep: str) -> JSONResponse:
    if not validate_cep(cep):
        raise ValueError("Invalid CEP")

    client = httpx.AsyncClient(verify=False)
    response: Response = await client.get(f"{BASE_URL}/{cep}")

    try:
        response.raise_for_status()
    except Exception:
        return JSONResponse(status_code=response.status_code, content=response.json())

    parsed_response = CepApiSuccess(**response.json())
    address = Address.from_response(parsed_response)
    return JSONResponse(status_code=200, content=jsonable_encoder(address))
