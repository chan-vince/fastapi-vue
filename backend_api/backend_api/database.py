import logging
import os
import sys
from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger("Database")
logging.basicConfig(
        format="%(asctime)s: %(levelname)s: %(name)s - %(message)s", level="DEBUG"
    )

DB_HOST = os.environ.get("DB_HOST")
if DB_HOST is None:
    DB_HOST = "127.0.0.1"

DB_PORT = os.environ.get("DB_PORT")
if DB_PORT is None:
    DB_PORT = 3306
else:
    DB_PORT = int(os.environ.get("DB_PORT"))

DB_NAME = os.environ.get("DB_NAME")
if DB_NAME is None:
    DB_NAME = "francis"

logger.info(f"Connecting to {DB_HOST}@{DB_PORT}/{DB_NAME}..")

DB_PASSWORD = os.environ.get("DB_PASSWORD")
if DB_PASSWORD is None:
    logger.error(f"MYSQL_PASSWORD is not set!")
    sys.exit(1)

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://francis:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_timeout=30, pool_size=200, max_overflow=100, pool_recycle=120)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

inspector = inspect(engine)
table_names = inspector.get_table_names()
printable_tables = ', '.join([x for x in table_names])
logger.info(f"Tables: {table_names}")
logger.info(f"Printable Tables: {printable_tables}")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()