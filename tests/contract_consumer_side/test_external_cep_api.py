from pact import Pact, match
from httpx import AsyncClient, Response
from src.model.external.cep_api_types import CepApiSuccess
import pytest


@pytest.fixture(scope="session")
def pact() -> Pact:
    return Pact("onboarding-proj1", "brasilapi-cep")


@pytest.fixture(scope="session")
def client() -> AsyncClient:
    return AsyncClient(verify=False)


@pytest.mark.asyncio
async def test_cep_api_response(pact: Pact, client: AsyncClient):
    path: str = "/api/cep/v2/12345678"
    (
        pact.upon_receiving(f"GET {path}")
        .given("address exists")
        .with_request(method="GET", path=path)
        .will_respond_with(200)
        .with_body(
            {
                "cep": match.like("12345678"),
                "state": match.like("some state"),
                "city": match.like("some city"),
                "neighborhood": match.like("some neighborhood"),
                "street": match.like("some street"),
                "location": {
                    "type": "point",
                    "coordinates": {
                        "latitude": match.like("123"),
                        "longitude": match.like("123"),
                    },
                },
            }
        )
    )

    with pact.serve() as srv:
        response: Response = await client.get(f"{srv.url}{path}")
        CepApiSuccess(**response.json())  # tests if doesn't throw exception
