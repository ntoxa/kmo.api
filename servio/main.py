from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/cards/", response_model=schemas.Card)
def read_card(issuer_id: int, card_id: str, db: Session = Depends(get_db)):
    card =  crud.get_card(db, issuer_id, card_id)
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return card


@app.post("/cards2/", response_model=list[schemas.Card])
def read_cards(issuer_id: int, card_ids: list[str], db: Session = Depends(get_db)):
    return crud.get_cards(db, issuer_id, card_ids)


@app.get("/get_status_talons")
def read_status_talons(issuer_id: int, first_num: str, quantity: int, enabled: bool, db: Session = Depends(get_db)):
    """
    Возвращает список номеров из базы, определенных параметрами:

    - **issuer_id**: код эмитента (Число)
    - **first_num**: первый номер диапазона (Строка)
    - **quantity**: количество номеров вдиапазоне (Число)
    - **enabled**: статус талона (Булево)
    """
    result = crud.get_status_cards(db, issuer_id, first_num, quantity, enabled)
    return result
