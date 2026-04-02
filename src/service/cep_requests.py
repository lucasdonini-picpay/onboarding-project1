from src.model.cep_types import Cep, Address
from src.model.external.cep_api_types import CepApiSuccess
from src.model.env_settings import EnvSettings
import httpx

env = EnvSettings()
client = httpx.AsyncClient(verify=False)


async def request_address(cep: Cep) -> Address:
    response = await client.get(f"{env.cep_api_url}/{cep}")
    response.raise_for_status()
    success = CepApiSuccess(**response.json())
    return Address.from_response(success)
