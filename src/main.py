from src.model.Address import Address
from src.model.external.CepApiSuccess import CepApiSuccess
from src.model.Cep import Cep

from fastapi import FastAPI
from dotenv import load_dotenv
import os, httpx

load_dotenv()
BASE_URL: str = os.getenv("API_URL")

app = FastAPI()


@app.get("/test")
def test_connection():
    return {"message": "Connection successful!"}


@app.get("/cep/{cep}")
async def get_cep(cep: str):
    parsed_cep = Cep(value=cep)
    client = httpx.AsyncClient(verify=False)
    response = await client.get(f"{BASE_URL}/{parsed_cep.value}")
    response.raise_for_status()
    parsed_response = CepApiSuccess(**response.json())
    address = Address.from_response(parsed_response)
    return address
