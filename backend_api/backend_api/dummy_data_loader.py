import json
import logging
import pathlib

from backend_api import crud
from backend_api.database import SessionLocal
from . import pydantic_schemas as schemas

logger = logging.getLogger("DummyDataLoader")


class DummyDataLoader:
    def __init__(self):
        pass

    @staticmethod
    def write_gp_practice_mock_data(json_file: pathlib.Path):
        logger.info("Writing mock data for GP Practices..")

        with json_file.open() as file:
            data = json.loads(file.read())

        db = SessionLocal()

        for index, item in enumerate(data):
            try:
                crud.create_gp_practice(db, schemas.GPPracticeCreate(**item))
            except Exception as e:
                logger.debug(e)
                db.rollback()

        logger.info("..done.")

    @staticmethod
    def write_gp_address_mock_data(json_file: pathlib.Path):
        pass