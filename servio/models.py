from sqlalchemy import Column, String, Boolean, Integer, Date

from .database import Base

class Talon(Base):
    __tablename__ = "CARDIDS"

    issuer_id = Column(name="ISSUER_ID", type_=Integer, primary_key=True)
    card_id = Column(name="CARD_ID", type_=String, primary_key=True)
    enabled = Column(name="ENABLED", type_=Boolean)
    finaldate = Column(name="FINALDATE", type_=Date)
