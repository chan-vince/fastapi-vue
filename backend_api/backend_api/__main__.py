from .log_setup import *
import argparse
import os
import pathlib
import sys

import uvicorn

from backend_api.config import DB_HOST, DB_PORT, LOGGING_CONFIG
from backend_api.database_connection import Base, Engine
# import backend_api.database_connection
from backend_api.utils import check_port_open
from .dummy_data_loader import DummyDataLoader

# Get the command line arguments
parser = argparse.ArgumentParser(description='Backend API server for the ICE PoC')
parser.add_argument('-l', '--log_level', default=os.environ.get('LOG_LEVEL'),
                    help="DEBUG | INFO | WARNING | ERROR | CRITICAL")
parser.add_argument('-m', '--mock_data', action="store_true", help="Load mock data into tables on start")
args = parser.parse_args()

# Configure logging
if args.log_level is None:
    os.environ["LOG_LEVEL"] = "INFO"
else:
    os.environ["LOG_LEVEL"] = args.log_level

log_level = os.environ.get('LOG_LEVEL').upper()
logger = logging.getLogger()
logger.log(
    logger.getEffectiveLevel(), f"Logging set to {log_level}"
)

# Set the hot reload option if the logging level is DEBUG
reload = True if log_level.lower() == "debug" else False
logger.info(f"Hot reload enabled: {reload}")


if __name__ == '__main__':
    if not check_port_open(DB_HOST, DB_PORT, retries=10):
        sys.exit(1)

    Base.metadata.create_all(bind=Engine)

    # Load the mock data if necessary
    if os.environ.get("MOCK_DATA") is None:
        os.environ["MOCK_DATA"] = "false"

    if args.mock_data or os.environ.get("MOCK_DATA").lower() == "true":
        mock_data_base_path = pathlib.Path(pathlib.Path.cwd()) / ".." / "mock_data"

        ddl = DummyDataLoader()

        # Load dummy data for the tables
        ddl.write_practice_mock_data(mock_data_base_path / "practices.json")
        ddl.write_address_mock_data(mock_data_base_path / "addresses.json")
        ddl.write_job_title_mock_data(mock_data_base_path / "job_titles.json")
        ddl.write_employee_mock_data(mock_data_base_path / "employees.json")
        ddl.write_access_system_mock_data(mock_data_base_path / "access_systems.json")
        ddl.write_ip_range_mock_data(mock_data_base_path / "ip_ranges.json")
        ddl.assign_employees_to_practice()
        ddl.assign_partner_to_practice()
        ddl.assign_access_system_to_practice()

    access_log = True if log_level == "DEBUG" or log_level == "INFO" else False
    logger.info(f"Access log enabled: {access_log}")

    # Start the ASGI server
    logger.info("Starting uvicorn")
    uvicorn.run("backend_api.app:app",
                host="0.0.0.0", port=5000,
                log_level=log_level.lower(), reload=reload,
                access_log=access_log, log_config=LOGGING_CONFIG)
