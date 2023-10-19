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


@app.get("/talons", response_model=list[schemas.Talon])
def read_talons(issuer_id: int | None = None,
                offset: int = 0,
                limit: int = 100,
                db: Session = Depends(get_db)
                ):
    talons = crud.get_talons(db, issuer_id, offset, limit)
    return talons


@app.get("/talons/{talon_id}", response_model=schemas.Talon)
def read_talon(talon_id: str, issuer_id: int, db: Session = Depends(get_db)):
    """
    Инфо о талоне.
    """
    talon = crud.get_talon(db, talon_id, issuer_id)
    if talon is None:
        raise HTTPException(status_code=404, detail="Talon not found")
    return talon


#@app.get("/talons_quantity")
def read_talons_quantity(issuer_id: int,
                         enabled: bool,
                         talon_mask: str = "",
                         db: Session = Depends(get_db)
                         ):
    talon_mask += "%"
    pass


@app.post("/get_status_talons", response_model=list)
def read_status_talons(data: list[schemas.StatusRequest], db: Session = Depends(get_db)):
    """
    Возвращает список номеров из базы, определенных параметрами:

    - **issuer_id**: код эмитента (Число)
    - **first_num**: первый номер диапазона (Строка)
    - **quantity**: количество номеров вдиапазоне (Число)
    - **enabled**: статус талона (Булево)
    """
    result = list()
    for row in data:
        result.append(crud.get_status_cards(db, row.issuer_id, row.first_num, row.quantity, row.enabled))

    return result
