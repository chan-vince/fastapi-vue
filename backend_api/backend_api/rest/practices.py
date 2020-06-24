import logging
from typing import List

from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import backend_api.pydantic_schemas as schemas
from backend_api.crud import practices as crud_practices
from backend_api.database import get_db

logger = logging.getLogger("REST:Practices")

# Create a fastapi router for these REST endpoints
router = APIRouter()


@router.post("/practice/", response_model=schemas.Practice)
def add_new_practice(practice: schemas.PracticeCreate, db: Session = Depends(get_db)):
    practice = crud_practices.read_practice_by_name(db, practice.name)
    if practice:
        raise HTTPException(status_code=422, detail=f"GP Practice with name {practice.name} already registered")
    return crud_practices.create_practice(db=db, practice=practice)


@router.put("/practice/", response_model=schemas.Practice)
def update_practice(practice_id: int, practice: schemas.PracticeCreate, db: Session = Depends(get_db)):
    existing_practice = crud_practices.read_practice_by_id(db, practice_id)
    if existing_practice is None:
        raise HTTPException(status_code=404, detail=f"Could not find practice with id {practice_id}")

    return crud_practices.update_practice(db, practice_id, practice)


@router.get("/practice/", response_model=List[schemas.Practice])
def get_all_practices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    practices = crud_practices.read_practices_all(db, skip=skip, limit=limit)
    return practices


@router.get("/practice/id/", response_model=schemas.Practice)
def get_practice_by_id(practice_id: int, db: Session = Depends(get_db)):
    practice: schemas.Practice = crud_practices.read_practice_by_id(db, practice_id=practice_id)
    if practice is None:
        raise HTTPException(status_code=404, detail=f"GP Practice with id {practice_id} not found")
    return practice


@router.get("/practice/name/", response_model=schemas.Practice)
def get_practice_by_name(name: str, db: Session = Depends(get_db)):
    practice: schemas.Practice = crud_practices.read_practice_by_name(db, gp_name=name)
    if practice is None:
        raise HTTPException(status_code=404, detail=f"GP Practice with name {name} not found")
    return practice


# Delete an existing practice
@router.delete("/practice/", response_model=schemas.Practice)
def delete_existing_practice_by_id(practice_id: int, db: Session = Depends(get_db)):
    # Raises 404 if doesn't exist
    get_practice_by_id(practice_id, db)
    return crud_practices.delete_practice(db, practice_id)


# Add an Access System to a practice
@router.put("/practice/system/", response_model=schemas.Practice)
def add_access_system_to_practice_by_id(practice_id: int, access_system_id: int, db: Session = Depends(get_db)):
    # Raises 404 if doesn't exist
    get_practice_by_id(practice_id, db)
    access_system = crud_practices.get_access_system_by_id(db, access_system_id)

    return crud_practices.add_access_system_to_practice(db, practice_id, access_system)


@router.delete("/practice/system/", response_model=schemas.Practice)
def remove_access_system_from_practice_by_id(practice_id: int, access_system_id: int, db: Session = Depends(get_db)):
    return crud_practices.delete_access_system_from_practice(db, practice_id, access_system_id)