import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv("servio/.env")
db_host = os.getenv('DB_HOST')
db_path = os.getenv('DB_PATH')
db_user = os.getenv('DB_USER')
db_passwd = os.getenv('DB_PASSWD')
fb_lib = os.getenv('FB_LIB')

url = "firebird+fdb://{}:{}@{}/{}?charset=UTF8&fb_library_name={}".format(
    db_user,db_passwd,db_host,db_path,fb_lib)

SQLALCHEMY_DATABASE_URL = url

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
