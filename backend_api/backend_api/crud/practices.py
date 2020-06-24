from sqlalchemy.orm import Session

from backend_api import database_models as tables
from backend_api import pydantic_schemas as schemas
from backend_api.pydantic_schemas import PracticeCreate


def read_practices_all(db: Session, skip, limit):
    return db.query(tables.Practice).offset(skip).limit(limit).all()


def read_practice_by_id(db: Session, practice_id: int):
    return db.query(tables.Practice).filter(tables.Practice.id == practice_id).first()


def read_practice_by_name(db: Session, practice_name: str):
    return db.query(tables.Practice).filter(tables.Practice.name == practice_name).first()


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


def get_all_access_systems(db: Session):
    return db.query(tables.AccessSystem).all()


def add_access_system_to_practice(db: Session, practice_id: int, access_system: schemas.AccessSystem):
    practice: tables.Practice = read_practice_by_id(db, practice_id)
    practice.access_systems.append(access_system)
    db.add(practice)
    db.commit()
    return practice


def delete_access_system_from_practice(db: Session, practice_id: int, access_system_id: int):
    practice: tables.Practice = read_practice_by_id(db, practice_id)

    for index, system in enumerate(practice.access_systems):
        if system.id == access_system_id:
            practice.access_systems.pop(index)

    db.add(practice)
    db.commit()
    return practice


def add_ip_range(db: Session, new_ip_range: schemas.IPRangeCreate):
    ip_range = tables.IPRange(**new_ip_range.dict())
    db.add(ip_range)
    db.commit()
    db.refresh(ip_range)
    return ip_range
