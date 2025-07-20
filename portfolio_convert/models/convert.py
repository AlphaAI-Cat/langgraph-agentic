from pydantic import BaseModel
from typing import Optional
from enum import Enum

class Currency(Enum):
    EUR = "EUR"
    INR = "INR"


class PortfolioStateInr(BaseModel):
    amount_usd: float
    total_usd : Optional[float] = 0
    total_inr : Optional[float] = 0


class PortfolioStateGeneral(BaseModel):
    amount_usd : float
    total_usd : Optional[float] = 0
    target_currency : Optional[Currency] = Currency.INR
    total_amount : Optional[float] = 0


