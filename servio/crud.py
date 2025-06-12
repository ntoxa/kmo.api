import logging

from datetime import date
from sqlalchemy import and_, text
from sqlalchemy.orm import Session
from .models import firebird_models, sqlite_models
from . import schemas

logger = logging.getLogger("root").getChild(__name__)


def get_talon(db: Session, talon_id: str, issuer_id: int):
    return db.query(firebird_models.Talon).filter(
        and_(firebird_models.Talon.issuer_id == issuer_id,
             firebird_models.Talon.card_id == talon_id)
        ).first()


def get_talons(db: Session, issuer_id: int,  offset: int = 0, limit: int = 100):
    return db.query(firebird_models.Talon).filter(
        firebird_models.Talon.issuer_id == issuer_id
    ).offset(offset).limit(limit).all()


def get_talons_quantity(db: Session, issuer_id: int, prefix: schemas.FuelType, enabled: bool, unexpired: bool):
    prefix = prefix.value
    query = """
    SELECT
        COUNT(*)
    FROM (
            SELECT
                CARD_ID
            FROM CARDIDS
            WHERE
                ISSUER_ID = :issuer_id
                AND ENABLED = :enabled
    ) as sub
    WHERE
        CARD_ID STARTING WITH :prefix
    """
    if unexpired:
        query += "AND FINALDATE > (SELECT CURRENT_DATE FROM RDB$DATABASE)"
    with db.begin():
        stmt = text(query)

        params = {
            "issuer_id": issuer_id,
            "enabled": int(enabled),
            "prefix": prefix
        }

        result = db.execute(stmt, params).scalar()

        return result


def get_status_cards(db: Session, issuer_id: int, first_num: str, quantity: int, enabled: bool):
    stmt = text("""
    SELECT
        C.CARD_ID
    FROM
        GET_TALON_NUMBERS(:first_num, :quantity) AS N
    INNER JOIN
        CARDIDS AS C
        ON N.TALON = C.CARD_ID
        AND C.ENABLED = :enabled
        AND C.ISSUER_ID = :issuer_id
    """)
    params = {
        "first_num": int(first_num),
        "quantity": quantity,
        "enabled": int(enabled),
        "issuer_id": issuer_id
        }
    result = db.execute(stmt, params).all()
    result = [row[0] for row in result]
    return result


def get_total(db: Session, date: date):
    with db.begin():
        result =  db.query(sqlite_models.Total).filter(
            sqlite_models.Total.created_at == date).first()
    return result.data


def create_total(db: Session, data: str):
    with db.begin():
        total = sqlite_models.Total(data=data)
        db.add(total)
    db.refresh(total)
