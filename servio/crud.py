from sqlalchemy import and_, text
from sqlalchemy.orm import Session

from . import models, schemas


def get_card(db: Session, issuer_id: int, card_id: str):
    return db.query(models.Card).filter(
        and_(models.Card.issuer_id == issuer_id, models.Card.card_id == card_id)).first()


def get_cards(db: Session, issuer_id: int, card_ids: list[str]):
    return db.query(models.Card).filter(
        and_(models.Card.issuer_id == issuer_id, models.Card.card_id.in_(card_ids))).all()


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
    params = {"first_num": int(first_num),"quantity": quantity, "enabled": int(enabled), "issuer_id": issuer_id}
    result = db.execute(stmt, params).all()
    result = [row[0] for row in result]
    return result
