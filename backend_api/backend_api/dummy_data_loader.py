import json
import logging
import pathlib

from backend_api import crud
from backend_api.database import SessionLocal
from . import pydantic_schemas as schemas

logger = logging.getLogger("DummyDataLoader")


class DummyDataLoader:
    def __init__(self):
        self.db = SessionLocal()

    def write_gp_practice_mock_data(self, json_file: pathlib.Path):
        logger.info("Writing mock data for GP Practices..")

        with json_file.open() as file:
            data = json.loads(file.read())

        for index, item in enumerate(data, 1):
            try:
                crud.update_gp_practice(self.db, schemas.GPPracticeCreate(**item))
            except Exception as e:
                logger.debug(e)
                self.db.rollback()
        logger.info("..done.")

    def write_gp_address_mock_data(self, json_file: pathlib.Path):
        logger.info("Writing mock data for GP Addresses..")
        with json_file.open() as file:
            data = json.loads(file.read())

        for index, item in enumerate(data, 1):
            try:
                crud.update_gp_address_by_gp_practice_id(self.db, index, schemas.GPAddressCreate(**item))
            except Exception as e:
                logger.debug(f"{index} {e}")
                self.db.rollback()
        logger.info("..done.")

    def write_job_titles_mock_data(self, json_file: pathlib.Path):
        logger.info("Writing mock data for Job Titles...")
        with json_file.open() as file:
            data = json.loads(file.read())

        for index, item in enumerate(data, 1):
            try:
                crud.add_job_title(self.db, schemas.JobTitleCreate(**item))
            except Exception as e:
                raise
                logger.debug(f"{index} {e}")
                self.db.rollback()
        logger.info("..done.")

    def write_employee_mock_data(self, json_file: pathlib.Path):
        logger.info("Writing mock data for Employees...")
        with json_file.open() as file:
            data = json.loads(file.read())

        for index, item in enumerate(data, 1):
            try:
                crud.add_employee(self.db, schemas.EmployeeCreate(**item, active=True))
            except Exception as e:
                logger.debug(f"{index} {e}")
                self.db.rollback()
        logger.info("..done.")