import logging
from typing import List

from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import backend_api.exc
import backend_api.pydantic_schemas as schemas
from backend_api import database
from backend_api.database_connection import get_db_session

logger = logging.getLogger("REST:Practices")

# Create a fastapi router for these REST endpoints
router = APIRouter()


@router.get("/practice/all", response_model=List[schemas.Practice])
def get_all_practices(skip: int = 0, limit: int = 100, session: Session = Depends(get_db_session)):
    """
    Queries the database for practices, returns all column data for each practice. Default page limit is 100
    """

    logger.debug(f"Getting all practices: {skip=} {limit=}")

    # skip and limit allow pagination, and the results should be a list of practices
    practices: List[schemas.Practice] = database.read_practices_all(session, skip=skip, limit=limit)

    # If there are none, raise a not found HTTP status code
    if not practices:
        raise HTTPException(status_code=404, detail="Practices table contains no entries")

    return practices


@router.get("/practice/id", response_model=schemas.Practice)
def get_practice_by_id(practice_id: int, session: Session = Depends(get_db_session)):
    """
    Query for a single practice by it's row ID
    """
    logger.debug(f"Getting practice for ID {practice_id}")

    practice: schemas.Practice = database.read_practice_by_id(session, practice_id=practice_id)

    if practice is None:
        raise HTTPException(status_code=404, detail=f"GP Practice with id {practice_id} not found")

    return practice


@router.get("/practice/name", response_model=schemas.Practice)
def get_practice_by_name(name: str, session: Session = Depends(get_db_session)):
    practice: schemas.Practice = database.read_practice_by_name(session, practice_name=name)
    if practice is None:
        raise HTTPException(status_code=404, detail=f"GP Practice with name {name} not found")
    return practice


@router.get("/practice/address_id", response_model=schemas.Practice)
def get_practice_by_address_id(address_id: int, session: Session = Depends(get_db_session)):
    try:
        practice: schemas.Practice = database.read_practice_by_address_id(session, address_id=address_id)
    except backend_api.exc.AddressNotFoundError:
        raise HTTPException(status_code=404, detail=f"No address found with ID {address_id}")

    if practice is None:
        raise HTTPException(status_code=404, detail=f"No Practices associated with address {address_id}")
    return practice


@router.get("/practice/count", response_model=schemas.RowCount)
def get_total_number_practices(session: Session = Depends(get_db_session)):
    return schemas.RowCount(count=database.read_total_number_of_practices(session))


@router.get("/practice/name/all", response_model=schemas.EntityNames)
def get_names_of_practices(session: Session = Depends(get_db_session)):
    return schemas.EntityNames(names=database.read_all_practice_names(session))


@router.get("/practice/all_employees", response_model=schemas.EmployeesForPractice)
def get_all_employees_in_practice(practice_id: int, db: Session = Depends(get_db_session)):
    try:
        employees = database.get_all_employees_for_practice_id(db, practice_id)
    except backend_api.exc.EmployeeNotFoundError:
        employees = []

    return {"practice_id": practice_id, "employees": employees}


@router.get("/practice/all_main_partners", response_model=List[schemas.Employee])
def get_main_partners_for_practice(practice_id: int, db: Session = Depends(get_db_session)):
    try:
        employees = database.get_main_partners_for_practice_id(db, practice_id)
    except backend_api.exc.EmployeeNotFoundError:
        employees = []
    return employees


@router.get("/practice/name/address", response_model=List[schemas.Address])
def get_address_for_practice_by_name(practice_name: str, db: Session = Depends(get_db_session)):
    if database.read_practice_by_name(db, practice_name) is None:
        raise HTTPException(status_code=400, detail=f"No GP Practice with name {practice_name}")

    addresses: schemas.Address = database.get_address_by_practice_name(db, practice_name=practice_name)
    if not addresses:
        raise HTTPException(status_code=404, detail=f"No address for GP Practice with name {practice_name}")
    return addresses


@router.get("/practice/id/address", response_model=List[schemas.Address])
def get_address_for_practice_by_id(practice_id: int, db: Session = Depends(get_db_session)):
    if database.read_practice_by_id(db, practice_id) is None:
        raise HTTPException(status_code=400, detail=f"No GP Practice with id {practice_id}")

    addresses: schemas.Address = database.get_addresses_by_practice_id(db, practice_id)
    if not addresses:
        raise HTTPException(status_code=404, detail=f"No address for GP Practice with id {practice_id}")
    return addresses


# @router.post("/practice", response_model=schemas.Practice)
# def add_new_practice(practice: schemas.PracticeCreate, db: Session = Depends(get_db)):
#     practice_existing = crud_practices.read_practice_by_name(db, practice.name)
#     if practice_existing:
#         raise HTTPException(status_code=422, detail=f"GP Practice with name {practice.name} already registered")
#     return crud_practices.create_practice(db=db, practice=practice)
#
#
# @router.put("/practice", response_model=schemas.Practice)
# def update_practice(practice_id: int, practice: schemas.PracticeCreate, db: Session = Depends(get_db)):
#     existing_practice = crud_practices.read_practice_by_id(db, practice_id)
#     if existing_practice is None:
#         raise HTTPException(status_code=404, detail=f"Could not find practice with id {practice_id}")
#
#     return crud_practices.update_practice(db, practice_id, practice)
#
#
# # Delete an existing practice
# @router.delete("/practice", response_model=schemas.Practice)
# def delete_existing_practice_by_id(practice_id: int, db: Session = Depends(get_db)):
#     # Raises 404 if doesn't exist
#     get_practice_by_id(practice_id, db)
#     return crud_practices.delete_practice(db, practice_id)
#
#
# # Add an Access System to a practice
# @router.post("/practice/system", response_model=schemas.Practice)
# def set_access_systems_for_practice_by_id(practice_id: int, access_system_ids: List[int], db: Session = Depends(get_db)):
#     # Raises 404 if doesn't exist
#     get_practice_by_id(practice_id, db)
#
#     return crud_practices.set_access_systems_for_practice(db, practice_id, access_system_ids)
#
#
# @router.put("/practice/main_partner", response_model=schemas.Practice)
# def assign_a_main_partner_to_practice(practice_id: int, employee_id: int, db: Session = Depends(get_db)):
#     return crud_practices.assign_employee_as_main_partner_of_practice(db, employee_id, practice_id)
#
#
# @router.delete("/practice/main_partner", response_model=schemas.Practice)
# def unassign_a_main_partner_from_practice(practice_id: int, employee_id: int, db: Session = Depends(get_db)):
#     return crud_practices.unassign_employee_as_main_partner_of_practice(db, employee_id, practice_id)
