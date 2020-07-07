import socket
import logging
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
