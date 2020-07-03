from typing import Union

from sqlalchemy.orm import Session
import sqlalchemy.exc
import backend_api.exc
from backend_api import database_models as tables
from backend_api import pydantic_schemas as schemas
from backend_api.pydantic_schemas import PracticeCreate

from sqlalchemy import inspect

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


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
    record: tables.StagingPractice = db.query(tables.StagingPractice).filter(tables.StagingPractice.id == id).first()

    update_item = {
        "name": record.name,
        "national_code": record.national_code,
        "emis_cdb_practice_code": record.emis_cdb_practice_code,
        "go_live_date": record.go_live_date,
        "closed": record.closed
    }

    # If there is no link to an actual Practice, then it means we need to add a new one
    if record.source_id is None:
        practice_details = object_as_dict(record)
        del practice_details["last_modified"]
        del practice_details["source_id"]
        del practice_details["requestor_id"]
        del practice_details["approver_id"]
        del practice_details["approved"]
        del practice_details["id"]
        new_practice = tables.Practice(**practice_details)
        db.add(new_practice)
        db.commit()
        db.refresh(new_practice)
        # new_practice.name = record.name
        # new_practice.go_live_date = record.go_live_date
        # new_practice.emis_cdb_practice_code = record.emis_cdb_practice_code
        # new_practice.national_code = record.national_code
        # new_practice.closed = record.closed
        # new_practice.created_at = record.created_at

    # Use the record's source_id to find the real entry in the practice table
    db.query(tables.Practice).filter(tables.Practice.id == record.source_id).update(update_item)
    record.approved = approved
    db.add(record)
    db.commit()
    return record