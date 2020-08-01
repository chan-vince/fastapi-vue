from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from backend_api.config import DB_NAME, DB_PORT, DB_HOST, DB_PASSWORD
from .log_setup import logger

logger.info(f"Connecting to {DB_HOST}@{DB_PORT}/{DB_NAME}..")
db_conn_url = f"mysql+pymysql://francis:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
Engine = create_engine(db_conn_url, pool_timeout=30, pool_size=200, max_overflow=100, pool_recycle=120)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)
Base = declarative_base()

# inspector = inspect(engine)
# table_names = inspector.get_table_names()
# logger.debug(f"Available database tables: {', '.join(table_names)}")


def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
