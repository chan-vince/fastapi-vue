import logging

from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import backend_api.pydantic_schemas as schemas
from backend_api.crud import practices as crud_practices
from backend_api.crud import practice_addresses as crud_practice_addresses
from backend_api.rest.practices import get_practice_by_id
from backend_api.database import get_db

logger = logging.getLogger("REST:Practices")

# Create a fastapi router for these REST endpoints
router = APIRouter()


@router.post("/practice/address/{practice_id}", response_model=schemas.Address)
def add_address_for_practice_by_id(practice_id: int,
                                   new_address: schemas.AddressCreate,
                                   db: Session = Depends(get_db)):

    practice = get_practice_by_id(practice_id=practice_id, db=db)
    if practice is None:
        raise HTTPException(status_code=404, detail=f"No GP Practice with id {practice_id}")

    return crud_practice_addresses.create_address_for_practice(db, practice_id=practice_id, address=new_address)


@router.put("/practice/address/{practice_id}", response_model=schemas.Address)
def update_address_for_practice_by_id(practice_id: int, updated_address: schemas.AddressCreate, db: Session = Depends(get_db)):
    practice = get_practice_by_id(practice_id=practice_id, db=db)
    if practice is None:
        raise HTTPException(status_code=404, detail=f"No GP Practice with id {practice_id}")
    return crud_practice_addresses.update_address_by_practice_id(db, practice_id=practice_id, new_address=updated_address)


@router.get("/practice/address/{practice_name}", response_model=schemas.Address)
def get_practice_address_by_name(practice_name: str, db: Session = Depends(get_db)):
    if crud_practices.read_practice_by_name(db, practice_name) is None:
        raise HTTPException(status_code=400, detail=f"No GP Practice with name {practice_name}")

    address: schemas.Address = crud_practice_addresses.read_practice_by_name(db, practice_name=practice_name)
    if address is None:
        raise HTTPException(status_code=404, detail=f"No address for GP Practice with name {practice_name}")
    return address


@router.get("/practice/address/{practice_id}", response_model=schemas.Address)
def get_practice_address_by_id(practice_id: int, db: Session = Depends(get_db)):
    if crud_practices.read_practice_by_id(db, practice_id) is None:
        raise HTTPException(status_code=400, detail=f"No GP Practice with id {practice_id}")

    addresses: schemas.Address = crud_practice_addresses.get_addresses_by_practice_id(db, practice_id)
    if not addresses:
        raise HTTPException(status_code=404, detail=f"No address for GP Practice with id {practice_id}")
    return addresses


@router.delete("/practice/address/", response_model=schemas.Practice)
def delete_address_from_practice(practice_id: int, address_id: int, db: Session = Depends(get_db)):
    return crud_practice_addresses.delete_address_from_practice(db, address_id, get_practice_by_id(practice_id, db))
