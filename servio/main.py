from datetime import datetime, date
import logging
import json
from typing import Callable, Annotated

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request, Response, Query
from fastapi.routing import APIRoute
from sqlalchemy.orm import Session
from apscheduler.schedulers.background import BackgroundScheduler

from . import crud, models, schemas
from .database import SessionLocal, engine
from db import localdb


class LoggerRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def logging_handler(request: Request) -> Response:
            req_body = await request.body()
            response: Response = await original_route_handler(request)
            logger.info(req_body.decode())
            res_body = response.body
            logger.info(res_body.decode())
            return response

        return logging_handler


logger = logging.getLogger()
app = FastAPI()
router = APIRouter(route_class=LoggerRoute)
scheduler = BackgroundScheduler()


def scheduled_job():
    logger.info("Scheduled job executed")
    session: Session = next(get_db())
    row = dict()
    row["Аи92"] = crud.get_talons_quantity(session, 2, schemas.FuelType.gasoline92, True, False)
    row["Аи95"] = crud.get_talons_quantity(session, 2, schemas.FuelType.gasoline95, True, False)
    row["ДТ_10"] = crud.get_talons_quantity(session, 2, schemas.FuelType.diesel10, True, False)
    row["ДТ_20"] = crud.get_talons_quantity(session, 2, schemas.FuelType.diesel20, True, False)
    row["ДТЗ_10"] = crud.get_talons_quantity(session, 2, schemas.FuelType.wdiesel10, True, False)
    row["ДТЗ_20"] = crud.get_talons_quantity(session, 2, schemas.FuelType.wdiesel20, True, False)
    row["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dumped_row = json.dumps(row, ensure_ascii=False)
    localdb.write_record(datetime.now().strftime("%Y-%m-%d"), dumped_row)


scheduler.add_job(scheduled_job, 'cron', hour=7, minute=50)
# scheduler.add_job(scheduled_job, 'interval', minutes=2)


@app.on_event("startup")
def start_scheduler():
    scheduler.start()

@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/talons", response_model=list[schemas.Talon])
def read_talons(issuer_id: int,
                offset: int = 0,
                limit: int = 1000,
                db: Session = Depends(get_db)
                ):
    """
    Возвращает список номеров из базы, определенных параметрами:

    - **issuer_id**: код эмитента (Число)
    - **offset**: смещение выборки (Число)
    - **limit**: количество получаемых строк (Число)

    """
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


@app.get("/talons_quantity", response_model=int)
def read_talons_quantity(issuer_id: int = 2,
                         enabled: bool = True,
                         unexpired: bool = True,
                         talon_mask: schemas.FuelType = Query(...),
                         db: Session = Depends(get_db)
                         ):
    """
    Метод возвращает количество талонов.

    - **issuer_id**: код эмитента (Число)
    - **enabled**: статус талона, погашен/не погашен (Булево)
    - **unexpired**: статус талона, все номера/только с не истёкшим сроком (Булево)
    - **talon_mask**: маска талона (Строка)
    """
    return crud.get_talons_quantity(db, issuer_id, talon_mask, enabled, unexpired)


@app.get("/slivki", response_model=dict)
def read_active_talons(date: date):
    """
    Метод возвращает количество талонов по дате.

    - **date**: дата (Дата)
    """
    result = localdb.read_record(date)
    if result is None:
        raise HTTPException(status_code=404, detail="No records found")
    return json.loads(result[0])


@router.post("/get_status_talons", response_model=list)
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
        result.extend(crud.get_status_cards(
            db, row.issuer_id, row.card_id, row.quantity, row.enabled)
            )

    return result


app.include_router(router)
