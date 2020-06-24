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
def add_update_new_practice(practice: schemas.PracticeCreate, db: Session = Depends(get_db)):
    practice = crud_practices.get_practice_by_name(db, practice.name)
    if practice:
        raise HTTPException(status_code=400, detail=f"GP Practice with name {practice.name} already registered")
    return crud_practices.update_practice(db=db, updated_practice=practice)


@router.post("/practice/address/{practice_id}", response_model=schemas.Address)
def add_update_address_for_practice_by_id(practice_id: int,
                                          new_address: schemas.AddressCreate,
                                          db: Session = Depends(get_db)):

    practice = read_practice_by_id(practice_id=practice_id, db=db)
    if practice is None:
        raise HTTPException(status_code=404, detail=f"No GP Practice with id {practice_id}")

    return crud_practices.update_address_by_practice_id(db, practice_id=practice_id, new_address=new_address)


@router.get("/practice/", response_model=List[schemas.Practice])
def read_all_practices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    practices = crud_practices.get_practices_all(db, skip=skip, limit=limit)
    return practices


@router.get("/practice/id/", response_model=schemas.Practice)
def read_practice_by_id(practice_id: int, db: Session = Depends(get_db)):
    practice: schemas.Practice = crud_practices.get_practice_by_id(db, practice_id=practice_id)
    if practice is None:
        raise HTTPException(status_code=404, detail=f"GP Practice with id {practice_id} not found")
    return practice


@router.get("/practice/name/", response_model=schemas.Practice)
def read_practice_by_name(name: str, db: Session = Depends(get_db)):
    practice: schemas.Practice = crud_practices.get_practice_by_name(db, gp_name=name)
    if practice is None:
        raise HTTPException(status_code=404, detail=f"GP Practice with name {name} not found")
    return practice


@router.get("/practice/address/", response_model=schemas.Address)
def read_practice_address_by_name(name: str, db: Session = Depends(get_db)):
    if crud_practices.get_practice_by_name(db, name) is None:
        raise HTTPException(status_code=400, detail=f"No GP Practice with name {name}")

    address: schemas.Address = crud_practices.get_address_by_practice_name(db, practice_name=name)
    if address is None:
        raise HTTPException(status_code=404, detail=f"No address for GP Practice with name {name}")
    return address
