import os
import sys
import logging

logger = logging.getLogger("Config")


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

DB_PASSWORD = os.environ.get("DB_PASSWORD")
if DB_PASSWORD is None:
    logger.error(f"MYSQL_PASSWORD is not set!")
    sys.exit(1)

TABLE_NAMES = []