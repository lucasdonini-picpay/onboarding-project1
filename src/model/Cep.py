from pydantic import BaseModel, field_validator
import re

_VALIDATION_REGEX: str = r"^\d{5}-?\d{3}$"


class Cep(BaseModel):
    value: str

    @field_validator("value")
    @classmethod
    def validate_cep_format(cls, value: str):
        value = value.strip()
        if not re.match(_VALIDATION_REGEX, value):
            raise ValueError("Invalid CEP format")
        return value
