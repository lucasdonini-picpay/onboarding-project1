from pydantic import BaseModel

"""
API 400 response JSON:
{
    "name": "BadRequestError",
    "message": "CEP deve conter exatamente 8 dígitos",
    "type": "validation_error"
}

API 404 response JSON:
{
    "name": "NotFoundError",
    "message": "CEP NAO ENCONTRADO",
    "type": "service_error"
}

API 500 response JSON:
{
    "name": "InternalError",
    "message": "Erro interno no serviço de CEP",
    "type": "internal_error"
}
"""


class CepApiFailure(BaseModel):
    name: str
    message: str
    type: str

    @classmethod
    def from_json(cls, json: str) -> "CepApiFailure":
        return cls.model_validate_json(json)
