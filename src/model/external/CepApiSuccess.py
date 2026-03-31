from pydantic import BaseModel
from typing import Optional

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
    latitude: Optional[str] = ""
    longitude: Optional[str] = ""


class _Location(BaseModel):
    type: str
    coordinates: _Coordinate


class CepApiSuccess(BaseModel):
    cep: str
    state: str
    city: str
    neighborhood: str
    street: str
    location: _Location
