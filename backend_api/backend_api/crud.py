from sqlalchemy.orm import Session
import sqlalchemy.exc

from . import database_models as tables
from . import pydantic_schemas as schemas
from .pydantic_schemas import GPPracticeCreate


def get_gp_practices_all(db: Session, skip, limit):
    return db.query(tables.GPPractices).offset(skip).limit(limit).all()


def get_gp_practice_by_id(db: Session, gp_practice_id: int):
    return db.query(tables.GPPractices).filter(tables.GPPractices.id == gp_practice_id).first()


def get_gp_practice_by_name(db: Session, gp_name: str):
    return db.query(tables.GPPractices).filter(tables.GPPractices.name == gp_name).first()


def create_gp_practice(db: Session, gp_practice: GPPracticeCreate):
    gp_practice = tables.GPPractices(**gp_practice.dict())
    db.add(gp_practice)
    db.commit()
    db.refresh(gp_practice)
    return gp_practice


def get_gp_addresses_all(db: Session, skip, limit):
    return db.query(tables.GPAddresses).offset(skip).limit(limit).all()


def get_gp_address_by_gp_practice_name(db: Session, gp_practice_name: str):
    return get_gp_practice_by_name(db, gp_practice_name).address


def update_gp_address_by_gp_practice_id(db: Session, gp_practice_id: int, new_address: schemas.GPAddressCreate):
    gp_address: tables.GPAddresses = tables.GPAddresses(**new_address.dict(), gp_practice_id=gp_practice_id)

    try:
        db.add(gp_address)
        db.commit()
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        gp_address = db.query(tables.GPAddresses).filter(tables.GPAddresses.gp_practice_id == gp_practice_id).first()

        gp_address.line_1 = new_address.line_1
        gp_address.line_2 = new_address.line_2
        gp_address.town = new_address.town
        gp_address.county = new_address.county
        gp_address.postcode = new_address.postcode
        gp_address.dts_email = new_address.dts_email

        db.add(gp_address)
        db.commit()

    db.refresh(gp_address)
    return gp_address