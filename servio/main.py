import logging
from typing import Callable

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request, Response
from fastapi.routing import APIRoute
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine


class LoggerRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def logging_handler(request: Request) -> Response:
            req_body = await request.body()
            logger.info(req_body.decode())
            response: Response = await original_route_handler(request)
            res_body = response.body
            logger.info(res_body.decode())
            return response

        return logging_handler


logger = logging.getLogger()
app = FastAPI()
router = APIRouter(route_class=LoggerRoute)


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


@router.post("/get_status_talons", response_model=list)
#@app.post("/get_status_talons", response_model=list)
def read_status_talons(body: list[schemas.StatusRequest], db: Session = Depends(get_db)):
    """
    Возвращает список номеров из базы, определенных параметрами:

    - **issuer_id**: код эмитента (Число)
    - **card_id**: первый номер диапазона (Строка)
    - **quantity**: количество номеров вдиапазоне (Число)
    - **enabled**: статус талона (Булево)
    """
    result = list()
    for row in body:
        result.extend(crud.get_status_cards(db, row.issuer_id, row.card_id, row.quantity, row.enabled))

    return result


app.include_router(router)
