from model.Address import Address
from model.external.CepApiSuccess import CepApiSuccess, _Location, _Coordinate


def test_valid_data():
    response: CepApiSuccess = CepApiSuccess(
        cep="00000000",
        state="SP",
        city="São Paulo",
        neighborhood="Vila Leopoldina",
        street="Rua exemplo",
        location=_Location(
            type="Point", coordinates=_Coordinate(latitude="-20", longitude="-20")
        ),
    )

    address: Address = Address.from_response(response)

    assert address.cep == response.cep
    assert address.state == response.state
    assert address.city == response.city
    assert address.neighborhood == response.neighborhood
    assert address.street == response.street
    assert address.coordinates == "20°S 20°O"
