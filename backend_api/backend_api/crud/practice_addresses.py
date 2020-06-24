from sqlalchemy.orm import Session

from backend_api import database_models as tables
from backend_api import pydantic_schemas as schemas
from backend_api.crud.practices import read_practice_by_name, read_practice_by_id


def get_addresses_all(db: Session, skip, limit):
    return db.query(tables.Address).offset(skip).limit(limit).all()


def get_address_by_practice_name(db: Session, practice_name: str):
    return read_practice_by_name(db, practice_name).address


def get_addresses_by_practice_id(db: Session, practice_id: int):
    return read_practice_by_id(db, practice_id).addresses


def create_address_for_practice(db: Session, practice_id: int, address: schemas.AddressCreate):
    address = tables.Address(**address.dict(), practice_id=practice_id)
    db.add(address)
    db.commit()
    return address


def update_address_by_practice_id(db: Session, practice_id: int, new_address: schemas.AddressCreate):
    db.query(tables.Address).filter(tables.Address.practice_id == practice_id).update({**new_address.dict()})
    db.commit()
    return read_practice_by_id(db, practice_id)


def delete_address_from_practice(db: Session, address_id: int, practice: schemas.Practice):
    for index, address in enumerate(practice.addresses):
        if address.id == address_id:
            practice.addresses.pop(index)

    db.add(practice)
    db.commit()
    return practice