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

        latitude: float = float(response.location.coordinates.latitude)
        is_south: bool = latitude < 0

        longitude: float = float(response.location.coordinates.longitude)
        is_west: bool = longitude < 0

        coordinate: str = (
            f"{abs(latitude)}°{'S' if is_south else 'N'} "
            f"{abs(longitude)}°{'O' if is_west else 'L'}"
        )

        return Address(
            cep=cep,
            state=response.state,
            city=response.city,
            neighborhood=response.neighborhood,
            street=response.street,
            coordinates=coordinate,
        )
