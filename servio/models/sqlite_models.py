import datetime

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Date

SQLiteBase = declarative_base()


class Total(SQLiteBase):
    __tablename__ = "totals"

    id = Column(name="id", type_=Integer, primary_key=True)
    created_at = Column(name="created_at", type_=Date, default=datetime.date.today)
    data = Column(name="data", type_=String)
