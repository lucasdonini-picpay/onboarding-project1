from unittest.mock import AsyncMock, MagicMock
from pytest_mock import MockFixture
from httpx import HTTPStatusError
from datetime import datetime
import pytest

from src.model.exchange_types import ExchangeResponse, Currency
from src.service.exchange_requests import calculate_exchange

EXPECTED_200_RESPONSE = {
    "cotacoes": [
        {
            "paridade_compra": 1,
            "paridade_venda": 1,
            "cotacao_compra": 5.7702,
            "cotacao_venda": 5.7708,
            "data_hora_cotacao": "2025-02-13 10:04:26.424",
            "tipo_boletim": "ABERTURA",
        },
        {
            "paridade_compra": 1,
            "paridade_venda": 1,
            "cotacao_compra": 5.7977,
            "cotacao_venda": 5.7983,
            "data_hora_cotacao": "2025-02-13 11:06:24.909",
            "tipo_boletim": "INTERMEDIÁRIO",
        },
        {
            "paridade_compra": 1,
            "paridade_venda": 1,
            "cotacao_compra": 5.7826,
            "cotacao_venda": 5.7832,
            "data_hora_cotacao": "2025-02-13 12:08:26.215",
            "tipo_boletim": "INTERMEDIÁRIO",
        },
        {
            "paridade_compra": 1,
            "paridade_venda": 1,
            "cotacao_compra": 5.7624,
            "cotacao_venda": 5.763,
            "data_hora_cotacao": "2025-02-13 13:03:25.722",
            "tipo_boletim": "INTERMEDIÁRIO",
        },
        {
            "paridade_compra": 1,
            "paridade_venda": 1,
            "cotacao_compra": 5.7782,
            "cotacao_venda": 5.7788,
            "data_hora_cotacao": "2025-02-13 13:03:25.728",
            "tipo_boletim": "FECHAMENTO PTAX",
        },
    ],
    "moeda": "USD",
    "data": "2025-02-13",
}


@pytest.fixture
def mock_exchange_client_success(mocker: MockFixture):
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = EXPECTED_200_RESPONSE

    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response

    mocker.patch("src.service.exchange_requests.client", mock_client)
    return mock_client


@pytest.fixture
def mock_exchange_client_failure(mocker: MockFixture):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPStatusError(
        "error", request=MagicMock(), response=MagicMock()
    )

    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response

    mocker.patch("src.service.exchange_requests.client", mock_client)
    return mock_client


@pytest.mark.asyncio
async def test_calculate_exchange_returns_200_response(mock_exchange_client_success):
    currency: Currency = Currency.USD
    original_value: float = 10.0

    result: ExchangeResponse = await calculate_exchange(currency, original_value)

    expected_rate = EXPECTED_200_RESPONSE["cotacoes"][-1]
    assert (
        result.bid
        == original_value
        / expected_rate["cotacao_compra"]
        / expected_rate["paridade_compra"]
    )
    assert (
        result.ask
        == original_value
        / expected_rate["cotacao_venda"]
        / expected_rate["paridade_venda"]
    )
    assert result.bid_rate == expected_rate["cotacao_compra"]
    assert result.ask_rate == expected_rate["cotacao_venda"]
    assert result.rate_date == datetime.fromisoformat(
        expected_rate["data_hora_cotacao"]
    )
    assert result.currency == EXPECTED_200_RESPONSE["moeda"]


@pytest.mark.asyncio
async def test_calculate_exchange_returns_failure(mock_exchange_client_failure):
    currency: Currency = Currency.USD
    original_value: float = 0.0

    with pytest.raises(HTTPStatusError):
        await calculate_exchange(currency, original_value)
