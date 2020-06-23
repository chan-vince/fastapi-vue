from sqlalchemy.orm import Session

from . import database_models as tables
from .pydantic_schemas import GPPracticeCreate


def get_gp_practice_by_id(db: Session, gp_practice_id: int):
    return db.query(tables.GPPractices).filter(tables.GPPractices.id == gp_practice_id).first()


def get_gp_practice_by_name_ice(db: Session, gp_name_ice: str):
    return db.query(tables.GPPractices).filter(tables.GPPractices.name_ice == gp_name_ice).first()


def create_gp_practice(db: Session, gp_practice: GPPracticeCreate):
    gp_practice = tables.GPPractices(**gp_practice.dict())
    db.add(gp_practice)
    db.commit()
    db.refresh(gp_practice)
    return gp_practice