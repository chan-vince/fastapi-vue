from typing import Union

from sqlalchemy.orm import Session
import sqlalchemy.exc
import backend_api.exc
from backend_api import database_models as tables
from backend_api import pydantic_schemas as schemas
from backend_api.pydantic_schemas import EmployeeCreate

from sqlalchemy import inspect


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


def update_staging_employee(db: Session, staging_employee: schemas.StagingEmployeeCreateRequest):

    existing_record_query = db.query(tables.StagingEmployee)\
        .filter(tables.StagingEmployee.source_id == staging_employee.source_id)\
        .filter(tables.StagingEmployee.approved == None)
    existing_record = existing_record_query.first()

    # If there's no existing staging record, create and insert one
    if existing_record is None:
        new_entry = tables.StagingEmployee(**staging_employee.dict())
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        return db.query(tables.StagingEmployee).filter(tables.StagingEmployee.id == new_entry.id).first()

    # Update the existing pending record with updated values
    existing_record_query.update({**staging_employee.dict()})
    db.commit()
    return existing_record


def add_new_staging_employee(db: Session, staging_employee: schemas.StagingEmployeeCreateRequest):
    entry = tables.StagingEmployee(**staging_employee.dict())
    db.add(entry)
    db.commit()
    return entry


def read_staging_employee(db: Session, staging_employee: schemas.StagingEmployeeRequest):
    return db.query(tables.StagingEmployee).filter(tables.StagingEmployee.source_id == staging_employee.source_id).first()


def read_all_staging_employees(db: Session, skip: int, limit: int):
    return db.query(tables.StagingEmployee).offset(skip).limit(limit).all()


def read_staging_employees_count_pending(db: Session):
    return db.query(tables.StagingEmployee).filter(tables.StagingEmployee.approved == None).count()


def action_pending_changes_to_employee_by_id(db: Session, id: int, approved: Union[bool, None]):
    record: tables.StagingEmployee = db.query(tables.StagingEmployee).filter(tables.StagingEmployee.id == id).first()

    update_item = {
        "name": record.name,
        "email": record.email,
        "job_title_id": record.job_title_id,
        "professional_num": record.professional_num,
        "it_portal_num": record.it_portal_num,
        "desktop_num": record.desktop_num,
        "active": record.active
    }

    # If there is no link to an actual employee, then it means we need to add a new one
    if record.source_id is None:
        employee_details = object_as_dict(record)
        del employee_details["last_modified"]
        del employee_details["source_id"]
        del employee_details["requestor_id"]
        del employee_details["approver_id"]
        del employee_details["approved"]
        del employee_details["id"]
        new_employee = tables.Employee(**employee_details)
        db.add(new_employee)
        db.commit()
        db.refresh(new_employee)
        # new_employee.name = record.name
        # new_employee.go_live_date = record.go_live_date
        # new_employee.emis_cdb_employee_code = record.emis_cdb_employee_code
        # new_employee.national_code = record.national_code
        # new_employee.closed = record.closed
        # new_employee.created_at = record.created_at

    # Use the record's source_id to find the real entry in the employee table
    db.query(tables.Employee).filter(tables.Employee.id == record.source_id).update(update_item)
    record.approved = approved
    db.add(record)
    db.commit()
    return record