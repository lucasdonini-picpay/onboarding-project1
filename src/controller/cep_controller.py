from fastapi import APIRouter
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from httpx import Response
import httpx, os

from src.model.external.CepApiSuccess import CepApiSuccess
from src.model.Address import Address
from src.utils.cep_utils import validate_cep

load_dotenv()
BASE_URL = os.getenv("API_URL")
router = APIRouter()


@router.get("/cep/{cep}")
async def get_cep(cep: str) -> JSONResponse:
    if not BASE_URL:
        raise RuntimeError("Missing environment variable: BASE_URL")

    if not validate_cep(cep):
        raise ValueError("Invalid CEP")

    response: Response
    client = httpx.AsyncClient(verify=False)
    response = await client.get(f"{BASE_URL}/{cep}")
    try:
        response.raise_for_status()
        parsed_response = CepApiSuccess(**response.json())
        address = Address.from_response(parsed_response)
        return JSONResponse(status_code=200, content=address)
    except Exception:
        return JSONResponse(status_code=response.status_code, content=response.json())
