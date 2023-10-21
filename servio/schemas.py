from datetime import date

from pydantic import BaseModel


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
