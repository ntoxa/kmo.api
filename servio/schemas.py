from enum import Enum
from typing import Optional
from datetime import date

from pydantic import BaseModel


class FuelType(str, Enum):
    diesel20 = "720"
    diesel10 = "710"
    wdiesel20 = "620"
    wdiesel10 = "610"
    gasoline95 = "310"
    gasoline92 = "210"


class Talon(BaseModel):
    card_id: str
    issuer_id: int
    enabled: bool
    finaldate: date

    class Config:
        from_attributes = True


class StatusRequest(BaseModel):
    issuer_id: int
    card_id: str
    quantity: int
    enabled: bool
