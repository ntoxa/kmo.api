from sqlalchemy import and_, func, text
from sqlalchemy.orm import Session

from . import models, schemas


def get_talon(db: Session, talon_id: str, issuer_id: int):
    return db.query(models.Talon).filter(
        and_(models.Talon.issuer_id == issuer_id, models.Talon.card_id == talon_id)).first()


def get_talons(db: Session, issuer_id: int,  offset: int = 0, limit: int = 100):
    return db.query(models.Talon).filter(
        models.Talon.issuer_id == issuer_id).offset(offset).limit(limit).all()


def get_talons_quantity(db: Session, issuer_id: int, talon_mask: schemas.FuelType, enabled: bool, unexpired: bool):
    talon_mask = talon_mask.value + "%"
    with db.begin():
        if unexpired:
            return db.query(func.count(models.Talon.card_id)).filter(
                and_(
                    models.Talon.issuer_id == issuer_id,
                    models.Talon.card_id.like(talon_mask),
                    models.Talon.enabled == enabled,
                    models.Talon.finaldate > func.now()
                )
            ).scalar()
        return db.query(func.count(models.Talon.card_id)).filter(
            and_(
                models.Talon.issuer_id == issuer_id,
                models.Talon.card_id.like(talon_mask),
                models.Talon.enabled == enabled
            )
        ).scalar()


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
