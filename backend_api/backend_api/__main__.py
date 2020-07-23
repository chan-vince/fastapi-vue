import argparse
import logging
import os
import pathlib
import sys

import fastapi
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from backend_api import __version__
from backend_api.config import DB_HOST, DB_PORT
from backend_api.database_connection import BASE, ENGINE
from backend_api.utils import check_port_open, LOGGING_CONFIG
from .dummy_data_loader import DummyDataLoader
from .rest import practices, employees, practice_addresses, access_systems, staging_changes

# Create the root instance of a FastAPI app
app = fastapi.FastAPI(title="GP Access Systems PoC API", version=__version__)

origins = [
    "http://127.0.0.1:8081",
    "http://localhost:8081",
    "http://127.0.0.1:80",
    "http://localhost:80",
    "http://78.47.251.229:40093",
    "https://abys.prelim.cloud"
]


app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_origin_regex="https://.*\.prelim\.cloud",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(
    practices.router, tags=["Practices"], prefix=f"/api/v1"
)
# app.include_router(
#     practice_addresses.router, tags=["Practice Addresses"], prefix=f"/api/v1"
# )
app.include_router(
    employees.router, tags=["Employees"], prefix=f"/api/v1"
)
app.include_router(
    access_systems.router, tags=["Access Systems"], prefix=f"/api/v1"
)
# app.include_router(
#     staging_changes.router, tags=["Staging Unified"], prefix=f"/api/v1"
# )


def start():
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
    logger = logging.getLogger("main")
    logging.basicConfig(
        format="%(asctime)s: %(levelname)s: %(name)s - %(message)s", level=log_level
    )
    logger.log(
        logger.getEffectiveLevel(), f"Logging set to {log_level}"
    )

    # Set the hot reload option if the logging level is DEBUG
    reload = True if log_level.lower() == "debug" else False
    logger.info(f"Hot reload enabled: {reload}")

    if not check_port_open(DB_HOST, DB_PORT, retries=10):
        sys.exit(1)

    BASE.metadata.create_all(bind=ENGINE)

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
    logger.info(f"Access logging enabled: {access_log}")

    logger.info("Starting uvicorn")
    # Start the ASGI server
    uvicorn.run("backend_api.__main__:app",
                host="0.0.0.0", port=5000,
                log_level=log_level.lower(), reload=reload,
                access_log=access_log, log_config=LOGGING_CONFIG)


if __name__ == '__main__':
    start()
