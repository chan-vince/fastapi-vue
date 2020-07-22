import json
import logging
import pathlib

from backend_api.crud import practices, practice_addresses, employees
from backend_api.database import SessionLocal
from . import database_models as models
from . import pydantic_schemas as schemas

logger = logging.getLogger("DummyDataLoader")


class DummyDataLoader:
    def __init__(self):
        self.db = SessionLocal()

    def write_practice_mock_data(self, json_file: pathlib.Path):

        with json_file.open() as file:
            data = json.loads(file.read())

        logger.info(f"Writing mock data for {len(data)} Practices..")
        try:
            for index, item in enumerate(data, 1):
                practices.create_practice(self.db, schemas.PracticeCreate(**item))
            logger.info("..done.")

        except Exception as e:
            print(f"index")
            logger.debug(e)
            self.db.rollback()

    def write_address_mock_data(self, json_file: pathlib.Path):
        with json_file.open() as file:
            data = json.loads(file.read())

        logger.info(f"Writing mock data for {len(data)} Addresses..")
        try:
            for index, item in enumerate(data, 1):
                practice_addresses.create_address_for_practice(self.db, index, schemas.AddressCreate(**item))
            logger.info("..done.")

        except Exception as e:
            logger.debug(f"{index} {e}")
            self.db.rollback()

    def write_job_title_mock_data(self, json_file: pathlib.Path):
        with json_file.open() as file:
            data = json.loads(file.read())

        logger.info(f"Writing mock data for {len(data)} Job Titles...")
        try:
            for index, item in enumerate(data, 1):
                employees.add_job_title(self.db, schemas.JobTitleCreate(**item))
            logger.info("..done.")

        except Exception as e:
            self.db.rollback()

    def write_employee_mock_data(self, json_file: pathlib.Path):
        with json_file.open() as file:
            data = json.loads(file.read())

        logger.info(f"Writing mock data for {len(data)}  Employees...")
        employees.add_employee_bulk(self.db, [schemas.EmployeeCreate(**item, active=True) for item in data])
        # for index, item in enumerate(data, 1):
        #     try:
        #         employees.add_employee(self.db, schemas.EmployeeCreate(**item, active=True))
        #     except Exception as e:
        #         logger.debug(f"{index} {e}")
        #         self.db.rollback()
        #         raise
        logger.info("..done.")

    def write_access_system_mock_data(self, json_file: pathlib.Path):
        with json_file.open() as file:
            data = json.loads(file.read())

        logger.info(f"Writing mock data for {len(data)} Access Systems...")
        try:
            for index, item in enumerate(data, 1):
                practices.add_access_system(self.db, schemas.AccessSystemCreate(**item))
            logger.info("..done.")

        except Exception as e:
            logger.debug(f"{index} {e}")
            self.db.rollback()

    def write_ip_range_mock_data(self, json_file:pathlib.Path):
        with json_file.open() as file:
            data = json.loads(file.read())

        logger.info(f"Writing mock data for {len(data)}  IP Ranges...")
        try:
            for index, item in enumerate(data, 1):
                practices.add_ip_range(self.db, schemas.IPRangeCreate(**item))
            logger.info("..done.")
        except Exception as e:
            logger.debug(f"{index} {e}")
            self.db.rollback()

    def assign_employees_to_practice(self):
        # Go through each of the 5000 employees and assign them to one practice
        practice_id = 1
        practice = self.db.query(models.Practice).filter(models.Practice.id == practice_id).first()
        logger.info(f"Assigning 20 employees per practice...")
        try:
            for index, employee in enumerate(self.db.query(models.Employee).all(), 1):
                employee.practices = [practice]
                self.db.add(employee)
                if index % 20 == 0:
                    practice_id += 1
                    practice = self.db.query(models.Practice).filter(models.Practice.id == practice_id).first()

            self.db.commit()
            logger.info("..done.")
        except Exception as e:
            logger.debug(e)
            self.db.rollback()

    def assign_partner_to_practice(self):
        logger.info("Assigning one partner to each practice...")

        partners = self.db.query(models.Employee).filter(models.Employee.job_title_id == 7).limit(250).all()
        try:
            for practice, partner in zip(self.db.query(models.Practice).all(), partners):
                practice.main_partners = [partner]
                self.db.add(practice)

            self.db.commit()
            logger.info("..done.")
        except Exception as e:
            logger.debug(e)
            self.db.rollback()

    def assign_access_system_to_practice(self):
        logger.info("Assigning an access system to each practice...")

        try:
            for index, practice in enumerate(self.db.query(models.Practice).all(), 1):
                if index % 1 == 0:
                    practice.access_systems = [self.db.query(models.AccessSystem).filter(models.AccessSystem.id == 1).first()]
                if index % 2 == 0:
                    practice.access_systems = [self.db.query(models.AccessSystem).filter(models.AccessSystem.id == 2).first()]
                if index % 3 == 0:
                    practice.access_systems = [self.db.query(models.AccessSystem).filter(models.AccessSystem.id == 3).first()]
                self.db.add(practice)

            self.db.commit()
            logger.info("..done.")
        except Exception as e:
            logger.debug(e)
            self.db.rollback()
