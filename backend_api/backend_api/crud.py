from sqlalchemy.orm import Session

from . import database_models as tables, pydantic_schemas as schemas


# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()


def get_gp_practice(db: Session, gp_practice_id: int):
    return db.query(tables.GPPractices).filter(tables.GPPractices.id == gp_practice_id).first()