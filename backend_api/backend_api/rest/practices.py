import logging
from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import backend_api.exc
import backend_api.pydantic_schemas as schemas
from backend_api.crud import practices as crud_practices
from backend_api.database import get_db

logger = logging.getLogger("REST:Practices")

# Create a fastapi router for these REST endpoints
router = APIRouter()


@router.get("/practice", response_model=List[schemas.Practice])
def get_all_practices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    practices = crud_practices.read_practices_all(db, skip=skip, limit=limit)
    return practices


@router.get("/practice/id", response_model=schemas.Practice)
def get_practice_by_id(practice_id: int, db: Session = Depends(get_db)):
    practice: schemas.Practice = crud_practices.read_practice_by_id(db, practice_id=practice_id)
    if practice is None:
        raise HTTPException(status_code=404, detail=f"GP Practice with id {practice_id} not found")
    return practice


@router.get("/practice/name", response_model=schemas.Practice)
def get_practice_by_name(name: str, db: Session = Depends(get_db)):
    practice: schemas.Practice = crud_practices.read_practice_by_name(db, practice_name=name)
    if practice is None:
        raise HTTPException(status_code=404, detail=f"GP Practice with name {name} not found")
    return practice


@router.get("/practice/address_id", response_model=schemas.Practice)
def get_practice_by_address_id(address_id: int, db: Session = Depends(get_db)):
    try:
        practice: schemas.Practice = crud_practices.read_practice_by_address_id(db, address_id=address_id)
    except backend_api.exc.AddressNotFoundError:
        raise HTTPException(status_code=404, detail=f"No address found with ID {address_id}")

    if practice is None:
        raise HTTPException(status_code=404, detail=f"No Practices associated with address {address_id}")
    return practice


@router.get("/practice/count", response_model=schemas.RowCount)
def get_total_number_practices(db: Session = Depends(get_db)):
    return schemas.RowCount(count=crud_practices.read_total_number_of_practices(db))


@router.get("/practice/names", response_model=schemas.EntityNames)
def get_names_of_practices(db: Session = Depends(get_db)):
    return schemas.EntityNames(names=crud_practices.read_all_practice_names(db))


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
