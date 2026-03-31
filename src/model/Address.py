from pydantic import BaseModel
from typing import Optional
from src.model.external.CepApiSuccess import CepApiSuccess
from src.model.Cep import Cep


class Address(BaseModel):
    cep: Cep
    state: str
    city: str
    neighborhood: str
    street: str
    coordinates: Optional[str]

    @classmethod
    def from_response(cls, response: CepApiSuccess) -> "Address":
        cep: Cep = Cep(value=response.cep)

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
            cep=cep,
            state=response.state,
            city=response.city,
            neighborhood=response.neighborhood,
            street=response.street,
            coordinates=coordinate,
        )
