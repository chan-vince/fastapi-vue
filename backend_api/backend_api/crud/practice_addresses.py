import sqlalchemy.exc
from sqlalchemy.orm import Session

import backend_api.exc
from backend_api import database_models as tables
from backend_api import pydantic_schemas as schemas
from backend_api.crud.practices import read_practice_by_name, read_practice_by_id


def get_addresses_all(db: Session, skip, limit):
    return db.query(tables.Address).offset(skip).limit(limit).all()


def read_address_by_id(db: Session, address_id: int):
    return db.query(tables.Address).filter(tables.Address.id == address_id).first()


def get_address_by_practice_name(db: Session, practice_name: str):
    return read_practice_by_name(db, practice_name).addresses


def get_addresses_by_practice_id(db: Session, practice_id: int):
    return read_practice_by_id(db, practice_id).addresses


def create_address_for_practice(db: Session, practice_id: int, address: schemas.AddressCreate):
    address = tables.Address(**address.dict(), practice_id=practice_id)
    db.add(address)
    db.commit()
    return address


def update_address_by_practice_id(db: Session, practice_id: int, address_id: int, new_address: schemas.AddressCreate):
    # Get the address
    address_query = db.query(tables.Address).filter(tables.Address.id == address_id)

    address: schemas.Address = address_query.first()
    # Make sure it is linked to the given practice
    if address.practice_id != practice_id:
        raise AssertionError

    # Update the address
    address_query.update({**new_address.dict()})

    db.commit()
    db.refresh(address)
    return address


def delete_address_from_practice(db: Session, address_id: int, practice: schemas.Practice):
    for index, address in enumerate(practice.addresses):
        if address.id == address_id:
            practice.addresses.pop(index)

    db.add(practice)
    db.commit()
    return practice


def assign_ip_range_to_address(db: Session, ip_range: schemas.IPRangeCreate):
    address: tables.Address = read_address_by_id(db, ip_range.address_id)
    if address is None:
        raise backend_api.exc.AddressNotFoundError

    ip_range = tables.IPRange(**ip_range.dict())
    db.add(ip_range)
    db.commit()
    return address


def modify_ip_range_for_address(db: Session, ip_range_id: int, cidr: str):
    ip_range: tables.IPRange = db.query(tables.IPRange).filter(tables.IPRange.id == ip_range_id).first()
    ip_range.cidr = cidr
    try:
        db.commit()
        return ip_range
    except sqlalchemy.exc.IntegrityError:
        raise backend_api.exc.IPRangeAlreadyExistsError


def unassign_ip_range_from_address(db: Session, ip_range_id: int, address_id: int):
    address: tables.Address = read_address_by_id(db, address_id)
    if address is None:
        raise backend_api.exc.AddressNotFoundError

    for index, ip in enumerate(address.ip_ranges):
        if ip.id == ip_range_id:
            address.ip_ranges.pop(index)

    db.add(address)
    db.commit()
    return address