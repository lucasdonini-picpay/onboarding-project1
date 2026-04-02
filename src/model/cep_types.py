from pydantic import BaseModel, AfterValidator
from typing import Optional, Annotated
from src.model.external.cep_api_types import CepApiSuccess
import re


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


def _validate_cep(value: str) -> str:
    if not re.match(r"\d{5}-?\d{3}", value):
        raise ValueError("Invalid CEP")
    return value


Cep = Annotated[str, AfterValidator(_validate_cep)]
