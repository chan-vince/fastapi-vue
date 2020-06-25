import sqlalchemy.exc
from sqlalchemy.orm import Session

from backend_api import database_models as tables
from backend_api import pydantic_schemas as schemas
import backend_api.exc
from backend_api.crud.practices import read_practice_by_id


def read_employee_by_email(db: Session, email: str):
    return db.query(tables.Employee).filter(tables.Employee.email == email).first()


def read_employee_by_id(db: Session, employee_id: int):
    return db.query(tables.Employee).filter(tables.Employee.id == employee_id).first()


def read_employee_by_professional_num(db: Session, professional_num: str):
    return db.query(tables.Employee).filter(tables.Employee.professional_num == professional_num).first()


def read_all_employees(db: Session, skip: int, limit: int):
    return db.query(tables.Employee).offset(skip).limit(limit).all()


def add_employee(db: Session, new_gp_employee: schemas.EmployeeCreate):
    employee: tables.Employee = tables.Employee(**new_gp_employee.dict())
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def update_employee(db: Session, employee_id: int, new_employee: schemas.EmployeeCreate):
    db.query(tables.Employee).filter(tables.Employee.id == employee_id).update({**new_employee.dict()})
    db.commit()
    return read_employee_by_id(db, employee_id)


def delete_employee(db: Session, employee_id: int):
    employee = read_employee_by_id(db, employee_id)
    db.delete(employee)
    db.commit()
    return employee


def assign_employee_to_practice(db: Session, employee_id: int, practice_id: int):
    employee: schemas.Employee = read_employee_by_id(db, employee_id)
    if employee is None:
        raise backend_api.exc.EmployeeNotFoundError

    practice = read_practice_by_id(db, practice_id)
    if practice is None:
        raise backend_api.exc.PracticeNotFoundError

    employee.practices.append(practice)
    db.add(employee)
    db.commit()
    return employee


def unassign_employee_from_all_practices(db: Session, employee_id: int):
    employee: schemas.Employee = read_employee_by_id(db, employee_id)
    if employee is None:
        raise backend_api.exc.EmployeeNotFoundError

    employee.practices = []
    db.add(employee)
    db.commit()
    return employee


def add_job_title(db: Session, new_job_title: schemas.JobTitleCreate):
    job_title = tables.JobTitle(**new_job_title.dict())
    try:
        db.add(job_title)
        db.commit()
        db.refresh(job_title)
    except sqlalchemy.exc.IntegrityError:
        db.rollback()

    return job_title


def modify_job_title_for_employee_id(db: Session, job_title_id: int, employee_id: int):
    job_title = db.query(tables.JobTitle).filter(tables.JobTitle.id == job_title_id).first()
    if job_title is None:
        raise backend_api.exc.JobTitleNotFoundError

    employee: schemas.Employee = read_employee_by_id(db, employee_id)
    if employee is None:
        raise backend_api.exc.EmployeeNotFoundError

    db.query(tables.Employee).filter(tables.Employee.id == employee_id).update({"job_title_id": job_title_id})
    db.commit()
    return employee
