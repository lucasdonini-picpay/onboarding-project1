from pact import Pact, match
from httpx import AsyncClient, Response
from src.model.external.exchange_api_types import ExchangeApiSuccess
import pytest


@pytest.fixture(scope="session")
def pact() -> Pact:
    return Pact("onboarding-proj1", "brasilapi-cambio")


@pytest.fixture(scope="session")
def client() -> AsyncClient:
    return AsyncClient(verify=False)


@pytest.mark.asyncio
async def test_exchange_api_response(pact: Pact, client: AsyncClient):
    path: str = f"/api/cambio/v1/cotacao/USD/2026-01-01T00:00:00.0000"
    (
        pact.upon_receiving(f"GET {path}")
        .given("exchange values exists")
        .with_request(method="GET", path=path)
        .will_respond_with(200)
        .with_body(
            {
                "cotacoes": match.each_like(
                    {
                        "paridade_compra": match.like(1),
                        "paridade_venda": match.like(1),
                        "cotacao_compra": match.like(1.1),
                        "cotacao_venda": match.like(1.1),
                        "data_hora_cotacao": match.like("2026-01-01 00:00:00.0000"),
                        "tipo_boletim": match.like("some type"),
                    }
                ),
                "moeda": match.like("USD"),
                "data": match.like("2026-01-01"),
            }
        )
    )

    with pact.serve() as srv:
        response: Response = await client.get(f"{srv.url}{path}")
        ExchangeApiSuccess(**response.json())  # tests if doesn't throw exception
