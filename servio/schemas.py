from datetime import datetime

from pydantic import BaseModel


class CardBase(BaseModel):
    card_id: str


class Talon(CardBase):
    issuer_id: int
    enabled: bool
    finaldate: datetime

    class Config:
        from_attributes = True


class StatusRequest(BaseModel):
    issuer_id: int
    card_id: str
    quantity: int
    enabled: bool
