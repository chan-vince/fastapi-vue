from sqlalchemy.orm import Session
from typing import List

import backend_api.exc
from backend_api import database_models as tables
from backend_api import pydantic_schemas as schemas
from backend_api.pydantic_schemas import PracticeCreate


def read_practices_all(db: Session, skip, limit):
    return db.query(tables.Practice).offset(skip).limit(limit).all()


def read_practice_by_id(db: Session, practice_id: int):
    return db.query(tables.Practice).filter(tables.Practice.id == practice_id).first()


def read_practice_by_name(db: Session, practice_name: str):
    return db.query(tables.Practice).filter(tables.Practice.name == practice_name).first()


def read_practice_by_address_id(db: Session, address_id: int):
    address = db.query(tables.Address).filter(tables.Address.id == address_id).first()

    if address is None:
        raise backend_api.exc.PracticeNotFoundError

    return db.query(tables.Practice).filter(tables.Practice.addresses.contains(address)).one()


def create_practice(db: Session, practice: schemas.PracticeCreate):
    practice = tables.Practice(**practice.dict())
    db.add(practice)
    db.commit()
    return practice


def update_practice(db: Session, practice_id: int, updated_practice: PracticeCreate):
    db.query(tables.Practice).filter(tables.Practice.id == practice_id).update({**updated_practice.dict()})
    db.commit()
    return read_practice_by_id(db, practice_id)


def delete_practice(db: Session, practice_id: int):
    practice = read_practice_by_id(db, practice_id)
    db.delete(practice)
    db.commit()
    return practice


def add_access_system(db: Session, new_access_system: schemas.AccessSystemCreate):
    access_system = tables.AccessSystem(**new_access_system.dict())
    db.add(access_system)
    db.commit()
    db.refresh(access_system)
    return access_system


def delete_access_system(db: Session, access_system_id: int):
    access_system = get_access_system_by_id(db, access_system_id)
    db.delete(access_system)
    db.commit()
    return access_system


def get_access_system_by_id(db: Session, access_system_id: int):
    return db.query(tables.AccessSystem).filter(tables.AccessSystem.id == access_system_id).first()


def get_all_access_systems(db: Session):
    return db.query(tables.AccessSystem).all()


def set_access_systems_for_practice(db: Session, practice_id: int, access_system_ids: List[int]):
    practice: tables.Practice = read_practice_by_id(db, practice_id)

    # Clear access systems
    practice.access_systems = []

    # Set all the ones in the list
    for as_id in access_system_ids:
        system = db.query(tables.AccessSystem).filter(tables.AccessSystem.id == as_id).first()
        practice.access_systems.append(system)

    db.add(practice)
    db.commit()
    return practice


def add_ip_range(db: Session, new_ip_range: schemas.IPRangeCreate):
    ip_range = tables.IPRange(**new_ip_range.dict())
    db.add(ip_range)
    db.commit()
    db.refresh(ip_range)
    return ip_range


def assign_employee_as_main_partner_of_practice(db: Session, employee_id: int, practice_id: int):
    employee: tables.Employee = db.query(tables.Employee).filter(tables.Employee.id == employee_id).first()

    if employee is None:
        raise backend_api.exc.EmployeeNotFoundError

    practice: tables.Practice = read_practice_by_id(db, practice_id)
    if practice is None:
        raise backend_api.exc.PracticeNotFoundError

    practice.main_partners.append(employee)
    db.add(practice)
    db.commit()
    return practice


def unassign_employee_as_main_partner_of_practice(db: Session, employee_id: int, practice_id: int):
    practice: tables.Practice = read_practice_by_id(db, practice_id)
    if practice is None:
        raise backend_api.exc.PracticeNotFoundError

    for index, employee in enumerate(practice.main_partners):
        if employee.id == employee_id:
            practice.main_partners.pop(index)

    return practice


def read_total_number_of_practices(db: Session):
    return db.query(tables.Practice).count()


def read_all_practice_names(db: Session):
    return [practice.name for practice in db.query(tables.Practice.name).all()]
