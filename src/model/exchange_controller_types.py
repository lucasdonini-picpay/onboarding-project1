from pydantic import BaseModel
from datetime import datetime


class ExchangeRequest(BaseModel):
    original_value: float
    target_currency: str


class ExchangeResponse(BaseModel):
    original_value: float
    original_currency: str
    value: float
    currency: str
    exchange_rate: float
    exchange_rate_date: datetime
