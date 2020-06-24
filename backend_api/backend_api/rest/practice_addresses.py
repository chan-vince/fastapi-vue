import logging

from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import backend_api.pydantic_schemas as schemas
from backend_api.crud import practices as crud_practices
from backend_api.crud import practice_addresses as crud_practice_addresses
from backend_api.rest.practices import read_practice_by_id
from backend_api.database import get_db

logger = logging.getLogger("REST:Practices")

# Create a fastapi router for these REST endpoints
router = APIRouter()


@router.post("/practice/address/{practice_id}", response_model=schemas.Address)
def add_update_address_for_practice_by_id(practice_id: int,
                                          new_address: schemas.AddressCreate,
                                          db: Session = Depends(get_db)):

    practice = read_practice_by_id(practice_id=practice_id, db=db)
    if practice is None:
        raise HTTPException(status_code=404, detail=f"No GP Practice with id {practice_id}")

    return crud_practice_addresses.update_address_by_practice_id(db, practice_id=practice_id, new_address=new_address)


@router.put("/practice/address/{practice_id}", response_model=schemas.Address)
def update_address_for_practice_by_id(practice_id: int, updated_address: schemas.AddressCreate, db: Session = Depends(get_db)):
    practice = read_practice_by_id(practice_id=practice_id, db=db)
    if practice is None:
        raise HTTPException(status_code=404, detail=f"No GP Practice with id {practice_id}")
    return crud_practice_addresses.update_address_by_practice_id(db, practice_id=practice_id, new_address=updated_address)


@router.get("/practice/address/{practice_name}", response_model=schemas.Address)
def read_practice_address_by_name(practice_name: str, db: Session = Depends(get_db)):
    if crud_practices.read_practice_by_name(db, practice_name) is None:
        raise HTTPException(status_code=400, detail=f"No GP Practice with name {practice_name}")

    address: schemas.Address = crud_practice_addresses.read_practice_by_name(db, practice_name=practice_name)
    if address is None:
        raise HTTPException(status_code=404, detail=f"No address for GP Practice with name {practice_name}")
    return address


@router.get("/practice/address/{practice_id}", response_model=schemas.Address)
def read_practice_address_by_id(practice_id: int, db: Session = Depends(get_db)):
    if crud_practices.read_practice_by_id(db, practice_id) is None:
        raise HTTPException(status_code=400, detail=f"No GP Practice with id {practice_id}")

    address: schemas.Address = crud_practice_addresses.get_address_by_practice_id(db, practice_id)
    if address is None:
        raise HTTPException(status_code=404, detail=f"No address for GP Practice with id {practice_id}")
    return address
