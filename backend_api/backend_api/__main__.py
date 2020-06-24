import argparse
import logging
import os
import pathlib

import fastapi
import uvicorn

from backend_api import __version__, database_models
from .database import engine
from .rest import practices, employees
from .dummy_data_loader import DummyDataLoader

database_models.Base.metadata.create_all(bind=engine)

# Create the root instance of a FastAPI app
app = fastapi.FastAPI(title="GP Access Systems PoC API", version=__version__)

app.include_router(
    practices.router, tags=["Practices"], prefix=f"/api/v1"
)
app.include_router(
    employees.router, tags=["Employees"], prefix=f"/api/v1"
)


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

    log_level = os.environ.get('LOG_LEVEL')
    logger = logging.getLogger()

    logging.basicConfig(
        format="%(asctime)s: %(levelname)s: %(name)s - %(message)s", level=log_level
    )
    logger.log(
        logger.getEffectiveLevel(), f"Logging set to {log_level}"
    )

    # Set the hot reload option if the logging level is DEBUG
    reload = True if log_level.lower() == "debug" else False
    logger.info(f"Hot reload enabled: {reload}")

    # Load the mock data if necessary
    if args.mock_data:
        mock_data_base_path = pathlib.Path(pathlib.Path.cwd()) / ".." / "mock_data"

        ddl = DummyDataLoader()

        # Load dummy data for the tables
        ddl.write_practice_mock_data(mock_data_base_path / "practices.json")
        ddl.write_address_mock_data(mock_data_base_path / "addresses.json")
        ddl.write_job_title_mock_data(mock_data_base_path / "job_titles.json")
        ddl.write_employee_mock_data(mock_data_base_path / "employees.json")
        ddl.write_access_system_mock_data(mock_data_base_path / "access_systems.json")
        ddl.write_ip_range_mock_data(mock_data_base_path / "ip_ranges.json")

    # Start the ASGI server
    uvicorn.run("backend_api.__main__:app", host="0.0.0.0", port=5000, log_level=log_level.lower(), reload=reload)


if __name__ == '__main__':

    # Start serving the API
    start()
