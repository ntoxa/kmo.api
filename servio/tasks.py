import json

from datetime import datetime
from sqlalchemy.orm import Session
from .db.firebird import fb_session
from .db.sqlite import sqlite_session
from .crud import get_talons_quantity, create_total
from .schemas import FuelType


def scheduled_job():
    fb_db: Session = fb_session()
    sqlite_db: Session = sqlite_session()
    row = dict()
    row["Аи92"] = get_talons_quantity(fb_db, 2, FuelType.gasoline92, True, False)
    row["Аи95"] = get_talons_quantity(fb_db, 2, FuelType.gasoline95, True, False)
    row["ДТ_10"] = get_talons_quantity(fb_db, 2, FuelType.diesel10, True, False)
    row["ДТ_20"] = get_talons_quantity(fb_db, 2, FuelType.diesel20, True, False)
    row["ДТЗ_10"] = get_talons_quantity(fb_db, 2, FuelType.wdiesel10, True, False)
    row["ДТЗ_20"] = get_talons_quantity(fb_db, 2, FuelType.wdiesel20, True, False)
    row["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dumped_row = json.dumps(row, ensure_ascii=False)
    try:
        create_total(sqlite_db, dumped_row)
    except Exception as e:
        print(f"Error creating total: {e}")
    finally:
        fb_db.close()
        sqlite_db.close()
