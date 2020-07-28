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

TABLE_NAMES = ""


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(asctime)s: %(levelprefix)s%(message)s",
            "use_colors": None,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(asctime)s: %(levelprefix)s%(client_addr)s - "%(request_line)s" %(status_code)s',
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "uvicorn": {"handlers": ["default"], "level": "INFO", "propagate": False},
        "uvicorn.error": {"level": "INFO", "propagate": True},
        "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
    },
}


OPENAPI_DESCRIPTION = """
Most if not all system data can be accessed with GET requests described here. There are few (if any) POST or 
PUT requests because ordinarily the data must go through an approval workflow before a change is committed 
to the database.

There are scenarios where a 'change request' does not need to be approved, and it can be committed to the 
database immediately. For these cases, the consumer of this API should make the request in the same way, regardless of
whether an approval is required or not. The backend will automatically approve a 'change request' if it does not need
prior approval.
"""