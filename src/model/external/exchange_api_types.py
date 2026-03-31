from pydantic import BaseModel
from typing import List
from datetime import date, datetime

"""
API 200 response JSON:
{
    "cotacoes": [
        {
            "paridade_compra": 1,
            "paridade_venda": 1,
            "cotacao_compra": 5.7702,
            "cotacao_venda": 5.7708,
            "data_hora_cotacao": "2025-02-13 10:04:26.424",
            "tipo_boletim": "ABERTURA"
        },
        { ... }
    ],
    "moeda": "USD",
    "data": "2025-02-13"
}
"""


class ExchangeValue(BaseModel):
    paridade_compra: int
    paridade_venda: int
    cotacao_compra: float
    cotacao_venda: float
    data_hora_cotacao: datetime
    tipo_boletim: str


class ExchangeApiSuccess(BaseModel):
    cotacoes: List[ExchangeValue]
    moeda: str
    data: date
