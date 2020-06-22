import logging

import fastapi
import uvicorn
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from backend_api import __version__, crud, database_models
from . import pydantic_schemas as schemas
from .database import SessionLocal, engine

database_models.Base.metadata.create_all(bind=engine)


# Create the root instance of a FastAPI app
app = fastapi.FastAPI(title="ICE PoC API", version=__version__)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# app.include_router(
    # jump_service.router, tags=["jump"], prefix=f"/api/{utils.get_config()['API']['VERSION']}"
# )


@app.get("/gp_practice/{gp_practice_id}", response_model=schemas.GPPractice)
def read_user(gp_practice_id: int, db: Session = Depends(get_db)):
    gp_practice = crud.get_gp_practice(db, gp_practice_id=gp_practice_id)
    if gp_practice is None:
        raise HTTPException(status_code=404, detail=f"GP Practice with id {gp_practice_id} not found")
    return gp_practice


def start():
    # Configure logging
    logger = logging.getLogger()

    # desired_log_level = utils.get_config()['General']['LogLevel']
    desired_log_level = "INFO"
    logging.basicConfig(
        format="%(asctime)s: %(levelname)s: %(name)s - %(message)s", level=desired_log_level
    )
    logger.log(
        logger.getEffectiveLevel(), f"Logging set to {desired_log_level}"
    )

    # Set the hot reload option if the logging level is DEBUG
    reload = True if desired_log_level.lower() == "debug" else False
    logger.info(f"Hot reload enabled: {reload}")

    # Start the ASGI server
    uvicorn.run("backend_api.__main__:app", host="0.0.0.0", port=5000, log_level=desired_log_level.lower(), reload=reload)


if __name__ == '__main__':

    # Todo some check to see if we should populate the database with test data

    # Start serving the API
    start()
