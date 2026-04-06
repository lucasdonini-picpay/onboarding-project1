from unittest.mock import AsyncMock, MagicMock
from pytest_mock import MockerFixture
from httpx import HTTPStatusError
import pytest

from src.service.cep_requests import request_address
from src.model.cep_types import Address, Cep

EXPECTED_200_RESPONSE = {
    "cep": "89010025",
    "state": "SC",
    "city": "Blumenau",
    "neighborhood": "Centro",
    "street": "Rua Doutor Luiz de Freitas Melro",
    "location": {
        "type": "Point",
        "coordinates": {"longitude": "-49.0629788", "latitude": "-26.9244749"},
    },
}


@pytest.fixture
def mock_cep_client_success(mocker: MockerFixture):
    mock_response = MagicMock()
    mock_response.json.return_value = EXPECTED_200_RESPONSE
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response

    mocker.patch("src.service.cep_requests.client", mock_client)
    return mock_client


@pytest.fixture
def mock_cep_client_failure(mocker: MockerFixture):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPStatusError(
        "error", request=MagicMock(), response=MagicMock()
    )

    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response

    mocker.patch("src.service.cep_requests.client", mock_client)
    return mock_client


@pytest.mark.asyncio
async def test_request_cep_returns_200_response(mock_cep_client_success):
    cep: Cep = Cep(EXPECTED_200_RESPONSE["cep"])
    expected_parsed_location: str = "26.9244749°S 49.0629788°O"

    result: Address = await request_address(cep)

    assert result.state == EXPECTED_200_RESPONSE["state"]
    assert result.city == EXPECTED_200_RESPONSE["city"]
    assert result.street == EXPECTED_200_RESPONSE["street"]
    assert result.neighborhood == EXPECTED_200_RESPONSE["neighborhood"]
    assert result.cep == EXPECTED_200_RESPONSE["cep"]
    assert result.coordinates == expected_parsed_location


@pytest.mark.asyncio
async def test_request_cep_returns_error(mock_cep_client_failure):
    cep: Cep = Cep("00000-000")

    with pytest.raises(HTTPStatusError):
        await request_address(cep)
