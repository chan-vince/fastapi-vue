from typing import Union

from sqlalchemy.orm import Session
import sqlalchemy.exc
import backend_api.exc
from backend_api import database_models as tables
from backend_api import pydantic_schemas as schemas
from backend_api.pydantic_schemas import PracticeCreate


def update_staging_practice(db: Session, staging_practice: schemas.StagingPracticeRequest):

    existing_record_query = db.query(tables.StagingPractice)\
        .filter(tables.StagingPractice.source_id == staging_practice.source_id)\
        .filter(tables.StagingPractice.approved == None)
    existing_record = existing_record_query.first()

    # If there's no existing staging record, create and insert one
    if existing_record is None:
        new_entry = tables.StagingPractice(**staging_practice.dict())
        db.add(new_entry)
        db.commit()
        return new_entry

    # Update the existing pending record with updated values
    existing_record_query.update({**staging_practice.dict()})
    db.commit()
    return existing_record


def read_staging_practice(db: Session, staging_practice: schemas.StagingPracticeRequest):
    return db.query(tables.StagingPractice).filter(tables.StagingPractice.source_id == staging_practice.source_id).first()


def read_all_staging_practices(db: Session, skip: int, limit: int):
    return db.query(tables.StagingPractice).offset(skip).limit(limit).all()


def read_staging_practices_count_pending(db: Session):
    return db.query(tables.StagingPractice).filter(tables.StagingPractice.approved == None).count()


def action_pending_changes_to_practice_by_id(db: Session, id: int, approved: Union[bool, None]):
    record: schemas.StagingRequest = db.query(tables.StagingPractice).filter(tables.StagingPractice.source_id == id).first()
    record.approved = approved
    db.add(record)
    db.commit()
    return record