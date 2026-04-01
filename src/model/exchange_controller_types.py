from pydantic import BaseModel
from datetime import datetime


class ExchangeResponse(BaseModel):
    bid: float
    ask: float
    currency: str
    bid_rate: float
    ask_rate: float
    rate_date: datetime
