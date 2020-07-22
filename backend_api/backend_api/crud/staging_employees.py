import sqlalchemy.exc
from sqlalchemy import inspect
from sqlalchemy.orm import Session
from typing import Union

import backend_api.exc
from backend_api import database_models as tables
from backend_api import pydantic_schemas as schemas
from backend_api.pydantic_schemas import EmployeeCreate


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


def update_staging_employee(db: Session, staging_employee: schemas.StagingEmployeeRequest):

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
    try:
        db.add(entry)
        db.commit()
        return entry
    except sqlalchemy.exc.IntegrityError:
        raise backend_api.exc.DuplicateEmployeeError


def read_staging_employee(db: Session, staging_employee: schemas.StagingEmployeeRequest):
    return db.query(tables.StagingEmployee).filter(tables.StagingEmployee.source_id == staging_employee.source_id).first()


def read_all_staging_employees(db: Session, skip: int, limit: int):
    return db.query(tables.StagingEmployee).offset(skip).limit(limit).all()


def read_staging_employees_count_pending(db: Session):
    return db.query(tables.StagingEmployee).filter(tables.StagingEmployee.approved == None).count()


def action_pending_changes_to_employee_by_id(db: Session, id: int, approved: Union[bool, None]):

    # Get the staging record details
    record: tables.StagingEmployee = db.query(tables.StagingEmployee).filter(tables.StagingEmployee.id == id).first()

    # Set approved value
    record.approved = approved
    db.add(record)
    db.commit()
    db.refresh(record)
    # Quit here if its rejected, no need to update more records
    if not approved:
        return record

    employee = {
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
        practice_name = employee_details["practice_name"]

        del employee_details["last_modified"]
        del employee_details["source_id"]
        del employee_details["requestor_id"]
        del employee_details["approver_id"]
        del employee_details["approved"]
        del employee_details["id"]
        del employee_details["practice_name"]
        new_employee = tables.Employee(**employee_details)
        new_employee.practices.append(db.query(tables.Practice).filter(tables.Practice.name == practice_name).first())
        db.add(new_employee)
        db.commit()
        db.refresh(new_employee)

    # Use the record's source_id to find the real entry in the employee table and update it
    db.query(tables.Employee).filter(tables.Employee.id == record.source_id).update(employee)

    record.approved = approved
    db.add(record)
    db.commit()
    return record