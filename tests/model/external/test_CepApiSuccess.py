from model.external.CepApiSuccess import CepApiSuccess
import json as js


def test_valid_data():
    json: str = """
{
    "cep": "89010025",
    "state": "SC",
    "city": "Blumenau",
    "neighborhood": "Centro",
    "street": "Rua Doutor Luiz de Freitas Melro",
    "location": {
        "type": "Point",
        "coordinates": {
            "longitude": "-49.0629788",
            "latitude": "-26.9244749"
        }
    }
}"""
    raw: dict = js.loads(json)
    response: CepApiSuccess = CepApiSuccess.from_json(json)

    assert response.cep == raw["cep"]
    assert response.state == raw["state"]
    assert response.city == raw["city"]
    assert response.neighborhood == raw["neighborhood"]

    location = response.location
    coordinates = location.coordinates

    assert location.type == raw["location"]["type"]
    assert coordinates.latitude == raw["location"]["coordinates"]["latitude"]
    assert coordinates.longitude == raw["location"]["coordinates"]["longitude"]
