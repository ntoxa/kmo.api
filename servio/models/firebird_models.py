from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Date

FirebirdBase = declarative_base()


class Talon(FirebirdBase):
    __tablename__ = "CARDIDS"

    issuer_id = Column(name="ISSUER_ID", type_=Integer, primary_key=True)
    card_id = Column(name="CARD_ID", type_=String(50), primary_key=True)
    enabled = Column(name="ENABLED", type_=Boolean)
    finaldate = Column(name="FINALDATE", type_=Date)
