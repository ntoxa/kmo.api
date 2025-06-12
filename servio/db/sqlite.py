import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

SQLITE_URL = f"sqlite:///{os.getenv('LOCALDB')}"
sqlite_engine = create_engine(SQLITE_URL, echo=False)
sqlite_session = sessionmaker(autocommit=False, autoflush=False, bind=sqlite_engine)
