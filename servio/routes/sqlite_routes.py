import json

from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from servio.dependencies import get_sqlite_db
from servio import crud

router = APIRouter()


@router.get("/slivki", response_model=dict)
def read_active_talons(date: date, db: Session = Depends(get_sqlite_db)):
    """
    Метод возвращает количество талонов по дате.

    - **date**: дата (Дата)
    """
    result = crud.get_total(db, date)
    if result is None:
        raise HTTPException(status_code=404, detail="No records found")
    return json.loads(result)
