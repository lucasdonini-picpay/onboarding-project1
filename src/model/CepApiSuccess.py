from pydantic import BaseModel

"""
API 200 repose JSON:
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
}
"""


class _Coordinate(BaseModel):
    latitude: str
    longitude: str


class _Location(BaseModel):
    type: str
    coordinates: _Coordinate


class CepApiSuccess(BaseModel):
    cep: str
    state: str
    city: str
    neighborhood: str
    street: str
    localtion: _Location

    @classmethod
    def from_json(cls, json: str) -> "CepApiSuccess":
        return cls.model_validate_json(json)
