from datetime import datetime
from pydantic import BaseModel


class CardBase(BaseModel):
    card_id: str


class Card(CardBase):
    issuer_id: int
    enabled: bool
    finaldate: datetime

    class Config:
        from_attributes = True
