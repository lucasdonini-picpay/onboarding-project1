import re

_VALIDATION_REGEX: str = r"^\d{5}-?\d{3}$"


def validate_cep(cep: str) -> bool:
    return re.match(_VALIDATION_REGEX, cep)
