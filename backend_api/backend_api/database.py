from sqlalchemy.orm import Session
from typing import List

import backend_api.exc
from backend_api import database_models as tables
from backend_api import pydantic_schemas as schemas
from backend_api.pydantic_schemas import PracticeCreate
import sqlalchemy.exc


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


def get_access_system_by_name(db: Session, name: str):
    return db.query(tables.AccessSystem).filter(tables.AccessSystem.name == name).first()


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


def create_address_for_practice(db: Session, practice_id: int, address: schemas.AddressCreate):
    # Create an address model and assign the practice_id
    address = tables.Address(**address.dict(), practice_id=practice_id)
    try:
        db.add(address)
        db.commit()
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        raise

    return address


def add_new_job_title(db: Session, new_job_title: schemas.JobTitleCreate):
    job_title = tables.JobTitle(**new_job_title.dict())
    try:
        db.add(job_title)
        db.commit()
        db.refresh(job_title)
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        raise

    return job_title


def add_many_employees(db: Session, new_gp_employees: List[schemas.EmployeeCreate]):
    db.bulk_save_objects([tables.Employee(**employee.dict()) for employee in new_gp_employees])
    db.commit()
    return


def read_employee_by_email(db: Session, email: str):
    return db.query(tables.Employee).filter(tables.Employee.email == email).first()


def add_employee(db: Session, new_gp_employee: schemas.EmployeeCreate):
    employee: tables.Employee = tables.Employee(**new_gp_employee.dict())
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def read_all_employees(db: Session, skip: int, limit: int):
    return db.query(tables.Employee).offset(skip).limit(limit).all()


def read_employee_by_id(db: Session, employee_id: int):
    return db.query(tables.Employee).filter(tables.Employee.id == employee_id).first()


def read_employee_by_name(db: Session, name: str):
    return db.query(tables.Employee).filter(tables.Employee.name == name).first()


def read_employee_by_professional_num(db: Session, professional_num: str):
    return db.query(tables.Employee).filter(tables.Employee.professional_num == professional_num).first()


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


def get_all_employees_for_practice_id(db: Session, practice_id: int):
    practice_employee = db.query(tables.association_practice_employee)\
        .filter(tables.association_practice_employee.columns.practice_id == practice_id)\
        .all()

    if len(practice_employee) == 0:
        raise backend_api.exc.EmployeeNotFoundError

    # Extract the list of employee IDs from the db results
    employee_ids = sorted([pair[1] for pair in practice_employee])

    # Get each employee in the list of IDs to get a list of the employee objects
    employees: List[schemas.Employee] = [read_employee_by_id(db, employee_id) for employee_id in employee_ids]
    return employees


def get_main_partners_for_practice_id(db: Session, practice_id: int):
    practice_partners = db.query(tables.association_practice_partners)\
        .filter(tables.association_practice_partners.columns.practice_id == practice_id)\
        .all()

    if len(practice_partners) == 0:
        raise backend_api.exc.EmployeeNotFoundError

    partners = sorted([pair[1] for pair in practice_partners])

    return [read_employee_by_id(db, employee_id) for employee_id in partners]


def get_all_job_titles(db: Session):
    return db.query(tables.JobTitle).all()


def read_total_number_of_employees(db: Session):
    return db.query(tables.Employee).count()


def read_all_employee_names(db: Session):
    return [employee.name for employee in db.query(tables.Employee.name).all()]


def get_address_by_practice_name(db: Session, practice_name: str):
    return read_practice_by_name(db, practice_name).addresses


def get_addresses_by_practice_id(db: Session, practice_id: int):
    return read_practice_by_id(db, practice_id).addresses
