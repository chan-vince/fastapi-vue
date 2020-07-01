from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://francis:{MYSQL_PASSWORD}@127.0.0.1:3306/francis"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_timeout=60, pool_recycle=120)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()