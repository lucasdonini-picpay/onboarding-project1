from fastapi import APIRouter
from dotenv import load_dotenv
import httpx, os

from src.model.external.CepApiSuccess import CepApiSuccess
from src.model.Address import Address
from src.utils.cep_utils import validate_cep

load_dotenv()
BASE_URL = os.getenv("API_URL")
router = APIRouter()


@router.get("/cep/{cep}")
async def get_cep(cep: str):
    if not BASE_URL:
        raise RuntimeError("Missing environment variable: BASE_URL")

    if not validate_cep(cep):
        raise ValueError("Invalid CEP")

    client = httpx.AsyncClient(verify=False)
    response = await client.get(f"{BASE_URL}/{cep}")
    response.raise_for_status()
    parsed_response = CepApiSuccess(**response.json())
    address = Address.from_response(parsed_response)
    return address
