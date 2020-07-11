import logging

import sqlalchemy.exc
from sqlalchemy import inspect
from sqlalchemy.orm import Session

import backend_api.exc
from backend_api import database_models as tables
from backend_api.database import Base
from backend_api.pydantic_schemas import StagingChangeRequest

logger = logging.getLogger("StagingChanges")


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


def id_exists(db: Session, table: str, id: int):
    for table_model in Base._decl_class_registry.values():
        if hasattr(table_model, '__tablename__') and table_model.__tablename__ == table:
            if db.query(table_model).filter(table_model.id == id).first() == None:
                return False
            return True
    else:
        return False


def get_table_model_by_name(table: str):
    for table_model in Base._decl_class_registry.values():
        if hasattr(table_model, '__tablename__') and table_model.__tablename__ == table:
            return table_model
    else:
        return None


def read_staging_record_by_id(db: Session, id: int):
    return db.query(tables.StagingChanges).filter(tables.StagingChanges.id == id).first()


def create_staging_record(db: Session, request: StagingChangeRequest):
    logger.debug("create_staging_record")

    if request.modify:
        raise AssertionError("Cannot create a new record if the modify flag is true")

    # Check for existing record with same target_table, target_id, and modify
    # existing_record_query = db.query(tables.StagingChanges)\
    #     .filter(tables.StagingChanges.target_table == request.target_table)\
    #     .filter(tables.StagingChanges.target_id == request.target_id)\
    #     .filter(tables.StagingChanges.modify == request.modify)
    #
    # existing_record = existing_record_query.first()
    #
    # if existing_record is not None:
    #     logger.debug(f"Updating existing record: {existing_record.id}")
    #     logger.debug(f"Request: {request.dict()}")
    #     existing_record_query.update(request.dict())
    #     record = existing_record
    # else:
    #     record = tables.StagingChanges(**request.dict())
    #     db.add(record)

    record = tables.StagingChanges(**request.dict())
    db.add(record)

    try:
        db.commit()
        return record

    except sqlalchemy.exc.IntegrityError:
        raise backend_api.exc.DuplicateStagingChangePayload


def modify_staging_record(db: Session, request: StagingChangeRequest):
    """
    Request to change the record of an existing entry in a table
    """

    if not request.modify:
        raise AssertionError("Modify requests should set modify to true")

    if request.target_id is None:
        raise AssertionError("target_id is required")

    table_model = get_table_model_by_name(request.target_table)

    record_query = db.query(table_model)\
        .filter(table_model.id == request.target_id)
    record = record_query.first()

    # the below for when we actually this is request and update the real record
    # Look for pending (approved = null) records which have a matching target table and id
    # record_query = db.query(tables.StagingChanges)\
    #     .filter(tables.StagingChanges.approved == None)\
    #     .filter(tables.StagingChanges.target_table == request.target_table)\
    #     .filter(tables.StagingChanges.target_id == request.target_id)

    if record is None:
        raise backend_api.exc.StagingChangeNotFoundError

    staging_record = tables.StagingChanges(**request.dict())

    # check for deltas, as potentially nothing actually changed
    for key, value in (request.payload.dict()).items():
        if record.__dict__.get(key) != value:
            logger.debug(f"Found a delta for {key}. Before: {record.__dict__.get(key)} After: {value}")
            break
    else:
        logger.debug("Request payload is identical to current state. Nothing to do")
        raise backend_api.exc.StagingChangeNoEffectError

    db.add(staging_record)

    try:
        db.commit()
        return staging_record
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        return db.query(tables.StagingChanges)\
            .filter(tables.StagingChanges.target_table == request.target_table)\
            .filter(tables.StagingChanges.target_id == request.target_id)\
            .first()


def read_all_staging_records(db: Session, skip: int, limit: int):
    return db.query(tables.StagingChanges).offset(skip).limit(limit).all()


def get_delta_for_record(db: Session, staging_id: int):
    # get the staging record
    staging_record = db.query(tables.StagingChanges).filter(tables.StagingChanges.id == staging_id).first()

    # find the table where the master record is
    table_model = get_table_model_by_name(staging_record.target_table)

    if staging_record.target_id is None:
        logger.debug("Staging record has no target id")
        delta = {key: {"current": None, "request": value} for key, value in staging_record.payload.items()}

    else:
        master_record = db.query(table_model).filter(table_model.id == staging_record.target_id).first()
        delta = {key: {"current": master_record.__dict__.get(key), "request": value} for key, value in staging_record.payload.items() if master_record.__dict__.get(key) != value}

    return {"deltas": delta}


def approve_staging_change(db: Session, staging_id: int, approver_id: int = 5000):
    """
    Approving means retrieving the staging record, and updating the main record, then marking this as approved.
    """
    # staging_record = db.query(tables.StagingChanges).filter(tables.StagingChanges.id)
    pass

def reject_staging_change(db: Session, staging_id: int):
    pass