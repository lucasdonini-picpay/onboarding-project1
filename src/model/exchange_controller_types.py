from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class ExchangeResponse(BaseModel):
    bid: float
    ask: float
    currency: str
    bid_rate: float
    ask_rate: float
    rate_date: datetime


class Currency(Enum):
    AUD = "AUD"
    CAD = "CAD"
    CHF = "CHF"
    DKK = "DKK"
    EUR = "EUR"
    GBP = "GBP"
    JPY = "JPY"
    SEK = "SEK"
    USD = "USD"
