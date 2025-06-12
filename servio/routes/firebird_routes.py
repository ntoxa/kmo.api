from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from servio.dependencies import get_fb_db
from servio import crud, schemas

router = APIRouter()


@router.get("/talons", response_model=list[schemas.Talon])
def read_talons(issuer_id: int,
                offset: int = 0,
                limit: int = 1000,
                db: Session = Depends(get_fb_db)
                ):
    """
    Возвращает список номеров из базы, определенных параметрами:

    - **issuer_id**: код эмитента (Число)
    - **offset**: смещение выборки (Число)
    - **limit**: количество получаемых строк (Число)

    """
    talons = crud.get_talons(db, issuer_id, offset, limit)
    return talons


@router.get("/talons/{talon_id}", response_model=schemas.Talon)
def read_talon(talon_id: str, issuer_id: int, db: Session = Depends(get_fb_db)):
    """
    Инфо о талоне.
    """
    talon = crud.get_talon(db, talon_id, issuer_id)
    if talon is None:
        raise HTTPException(status_code=404, detail="Talon not found")
    return talon


@router.get("/talons_quantity", response_model=int)
def read_talons_quantity(issuer_id: int = 2,
                         enabled: bool = True,
                         unexpired: bool = False,
                         prefix: schemas.FuelType = Query(...),
                         db: Session = Depends(get_fb_db)
                         ):
    """
    Метод возвращает количество талонов.

    - **issuer_id**: код эмитента (Число)
    - **enabled**: статус талона, погашен/не погашен (Булево)
    - **unexpired**: статус талона, все номера/только с не истёкшим сроком (Булево)
    - **prefix**: префикс талона (Строка)
    """
    return crud.get_talons_quantity(db, issuer_id, prefix, enabled, unexpired)


@router.post("/get_status_talons", response_model=list)
def read_status_talons(body: list[schemas.StatusRequest], db: Session = Depends(get_fb_db)):
    """
    Возвращает список номеров из базы, определенных параметрами:

    - **issuer_id**: код эмитента (Число)
    - **card_id**: первый номер диапазона (Строка)
    - **quantity**: количество номеров вдиапазоне (Число)
    - **enabled**: статус талона (Булево)
    """
    result = list()
    for row in body:
        result.extend(crud.get_status_cards(
            db, row.issuer_id, row.card_id, row.quantity, row.enabled)
            )

    return result
