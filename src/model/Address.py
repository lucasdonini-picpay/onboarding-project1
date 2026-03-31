from pydantic import BaseModel
from typing import Optional
from src.model.external.cep_api_types import CepApiSuccess


class Address(BaseModel):
    cep: str
    state: str
    city: str
    neighborhood: str
    street: str
    coordinates: Optional[str]

    @classmethod
    def from_response(cls, response: CepApiSuccess) -> "Address":
        coordinate: str = ""
        latitude: Optional[str] = response.location.coordinates.latitude
        longitude: Optional[str] = response.location.coordinates.longitude

        if latitude and longitude:
            is_south: bool = float(latitude) < 0
            is_west: bool = float(longitude) < 0
            coordinate = (
                f"{latitude.replace('-', '')}°{'S' if is_south else 'N'} "
                f"{longitude.replace('-', '')}°{'O' if is_west else 'L'}"
            )

        return Address(
            cep=response.cep,
            state=response.state,
            city=response.city,
            neighborhood=response.neighborhood,
            street=response.street,
            coordinates=coordinate if coordinate else None,
        )
