import json
import logging
import pathlib

import fastapi
import uvicorn

from backend_api import __version__, crud, database_models
from . import pydantic_schemas as schemas
from .database import engine, SessionLocal
from .rest import gp_practices

database_models.Base.metadata.create_all(bind=engine)


# Create the root instance of a FastAPI app
app = fastapi.FastAPI(title="ICE PoC API", version=__version__)

app.include_router(
    gp_practices.router, tags=["GP Practices"], prefix=f"/api/v1"
)


def start():
    # Configure logging
    logger = logging.getLogger()

    # desired_log_level = utils.get_config()['General']['LogLevel']
    desired_log_level = "DEBUG"
    logging.basicConfig(
        format="%(asctime)s: %(levelname)s: %(name)s - %(message)s", level=desired_log_level
    )
    logger.log(
        logger.getEffectiveLevel(), f"Logging set to {desired_log_level}"
    )

    # Set the hot reload option if the logging level is DEBUG
    reload = True if desired_log_level.lower() == "debug" else False
    logger.info(f"Hot reload enabled: {reload}")

    # Load the mock data if necessary
    mock_data_load = True

    if mock_data_load:
        with pathlib.Path(pathlib.Path.cwd() / ".." / "mock_data" / "gp_practices.json").open() as file:
            data = json.loads(file.read())

        db = SessionLocal()
        for index, item in enumerate(data):
            try:
                crud.create_gp_practice(db, schemas.GPPracticeCreate(**item))
            except Exception as e:
                print(e)
                db.rollback()
                print(f"{index} {item['emis_cdb_practice_code']}  {item['name']}")

    # Start the ASGI server
    uvicorn.run("backend_api.__main__:app", host="0.0.0.0", port=5000, log_level=desired_log_level.lower(), reload=reload)


if __name__ == '__main__':

    # Todo some check to see if we should populate the database with test data

    # Start serving the API
    start()
