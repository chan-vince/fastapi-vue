from sqlalchemy.orm import Session
import sqlalchemy.exc
import backend_api.exc
from backend_api import database_models as tables
from backend_api import pydantic_schemas as schemas
from backend_api.pydantic_schemas import PracticeCreate


def update_staging_practice(db: Session, staging_practice: schemas.StagingPracticeRequest):

    # If there's no existing staging record, create and insert one
    existing_record = read_staging_practice(db, staging_practice)
    if not existing_record:
        new_entry = tables.StagingPractice(**staging_practice.dict())
        db.add(new_entry)
        db.commit()
        return new_entry
    # Otherwise
    else:
        db.query(tables.StagingPractice).filter(tables.StagingPractice.source_id == staging_practice.source_id).update({**staging_practice.dict()})
        db.commit()
        return existing_record


def read_staging_practice(db: Session, staging_practice: schemas.StagingPracticeRequest):
    return db.query(tables.StagingPractice).filter(tables.StagingPractice.source_id == staging_practice.source_id).first()