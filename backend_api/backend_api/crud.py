from sqlalchemy.orm import Session
import sqlalchemy.exc

from . import database_models as tables
from . import pydantic_schemas as schemas
from .pydantic_schemas import GPPracticeCreate


def get_gp_practices_all(db: Session, skip, limit):
    return db.query(tables.GPPractices).offset(skip).limit(limit).all()


def get_gp_practice_by_id(db: Session, gp_practice_id: int):
    return db.query(tables.GPPractices).filter(tables.GPPractices.id == gp_practice_id).first()


def get_gp_practice_by_name(db: Session, gp_name: str):
    return db.query(tables.GPPractices).filter(tables.GPPractices.name == gp_name).first()


def update_gp_practice(db: Session, updated_gp_practice: GPPracticeCreate):
    gp_practice = tables.GPPractices(**updated_gp_practice.dict())

    try:
        db.add(gp_practice)
        db.commit()
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        gp_practice = get_gp_practice_by_name(db, updated_gp_practice.name)

        gp_practice.phone_num = updated_gp_practice.phone_num
        gp_practice.emis_cdb_practice_code = updated_gp_practice.emis_cdb_practice_code
        gp_practice.go_live_date = updated_gp_practice.go_live_date
        gp_practice.closed = updated_gp_practice.closed
        db.add(gp_practice)
        db.commit()

    db.refresh(gp_practice)
    return gp_practice


def get_gp_addresses_all(db: Session, skip, limit):
    return db.query(tables.GPAddresses).offset(skip).limit(limit).all()


def get_gp_address_by_gp_practice_name(db: Session, gp_practice_name: str):
    return get_gp_practice_by_name(db, gp_practice_name).address


def update_gp_address_by_gp_practice_id(db: Session, gp_practice_id: int, new_address: schemas.GPAddressCreate):
    gp_address: tables.GPAddresses = tables.GPAddresses(**new_address.dict(), gp_practice_id=gp_practice_id)

    try:
        db.add(gp_address)
        db.commit()
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        gp_address = db.query(tables.GPAddresses).filter(tables.GPAddresses.gp_practice_id == gp_practice_id).first()

        gp_address.line_1 = new_address.line_1
        gp_address.line_2 = new_address.line_2
        gp_address.town = new_address.town
        gp_address.county = new_address.county
        gp_address.postcode = new_address.postcode
        gp_address.dts_email = new_address.dts_email

        db.add(gp_address)
        db.commit()

    db.refresh(gp_address)
    return gp_address


def get_employee_by_email(db: Session, email: str):
    return db.query(tables.Employees).filter(tables.Employees.email == email).first()


def add_employee(db: Session, new_employee: schemas.EmployeeCreate):
    employee: tables.Employees = tables.Employees(**new_employee.dict())
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def update_employee(db: Session, employee_id: int, new_employee: schemas.Employee):

    employee = db.query(tables.Employees).filter(tables.Employees.id == employee_id).first().update(new_employee)

    employee.first_name = new_employee.first_name
    employee.last_name = new_employee.last_name
    employee.email = new_employee.email
    employee.professional_num = new_employee.professional_num
    employee.desktop_num = new_employee.desktop_num
    employee.it_portal_num = new_employee.it_portal_num
    employee.active = new_employee.active
    employee.job_title_id = new_employee.job_title_id

    db.add(employee)
    db.commit()

    db.refresh(employee)
    return employee


def add_job_title(db: Session, new_job_title: schemas.JobTitleCreate):
    job_title = tables.JobTitles(**new_job_title.dict())
    db.add(job_title)
    db.commit()
    db.refresh(job_title)
    return job_title
