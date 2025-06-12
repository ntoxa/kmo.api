from .db.firebird import fb_session
from .db.sqlite import sqlite_session


def get_fb_db():
    """
    Get a Firebird database session.
    """
    db = fb_session()
    try:
        yield db
    finally:
        db.close()


def get_sqlite_db():
    """
    Get a SQLite database session.
    """
    db = sqlite_session()
    try:
        yield db
    finally:
        db.close()
