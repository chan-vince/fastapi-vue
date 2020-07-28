import logging
import socket
import time

from backend_api.pydantic_schemas import EmployeeCreate, PracticeCreate, AddressCreate, IPRangeCreate
from backend_api.database_models import Employee, Practice, Address, IPRange


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


def get_pydantic_model_for_entity(name: str):
    classes = {
        "employee": EmployeeCreate,
        "practice": PracticeCreate,
        "address": AddressCreate,
        "ip_range": IPRangeCreate
    }
    return classes.get(name)


def get_sqlalchemy_model_for_entity(name: str):
    classes = {
        "employee": Employee,
        "practice": Practice,
        "address": Address,
        "ip_range": IPRange,
    }
    return classes.get(name)


def columns_to_dict(row):
    result = row.__dict__
    del result["_sa_instance_state"]
    return result
