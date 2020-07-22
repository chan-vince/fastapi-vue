import logging
from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from backend_api.config import DB_NAME, DB_PORT, DB_HOST, DB_PASSWORD, TABLE_NAMES

logger = logging.getLogger("Database")


logger.info(f"Connecting to {DB_HOST}@{DB_PORT}/{DB_NAME}..")
DB_CONN_URL = f"mysql+pymysql://francis:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

ENGINE = create_engine(DB_CONN_URL, pool_timeout=30, pool_size=200, max_overflow=100, pool_recycle=120)
SESSIONLOCAL = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
BASE = declarative_base()

INSPECTOR = inspect(ENGINE)
TABLE_NAMES += INSPECTOR.get_table_names()

logger.debug(f"Available database tables: {', '.join(TABLE_NAMES)}")


def get_db_session():
    db = SESSIONLOCAL()
    try:
        yield db
    finally:
        db.close()
