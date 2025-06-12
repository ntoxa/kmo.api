import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

FIREBIRD_URL = "firebird+fdb://{}:{}@{}/{}?charset=UTF8&fb_library_name={}".format(
    os.getenv('DB_USER'),
    os.getenv('DB_PASSWD'),
    os.getenv('DB_HOST'),
    os.getenv('DB_PATH'),
    os.getenv('FB_LIB')
)

fb_engine = create_engine(FIREBIRD_URL, echo=False)
fb_session = sessionmaker(autocommit=False, autoflush=False, bind=fb_engine)
