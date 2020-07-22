import logging
import socket
import time


def check_port_open(host: str, port: int, retries: int, interval: int = 5, logger: logging.Logger = None):

    if logger is None:
        logger = logging.getLogger("PortCheck")

    for count in range(1, retries + 1):
        s = socket.socket()
        try:
            s.connect((host, port))
            logger.info(f"Connected to {host} on port {port}")
            return True
        except socket.error:
            logger.error(f"Cannot connect to {host}:{port}, retrying..({count}/{retries})")
            time.sleep(interval)
        finally:
            s.close()
    else:
        logger.fatal(f"Connection to InfluxDB at {host}:{port} failed")
        return False


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
            "stream": "ext://sys.stderr",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "uvicorn": {"handlers": ["default"], "level": "INFO"},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
    },
}