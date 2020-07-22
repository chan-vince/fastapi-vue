import datetime
import json
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
    for name, model in Base.metadata.tables.items():
        if name == table:
            logger.debug(type(model))
            return model
    else:
        logger.debug("Not found")
        return None


def read_staging_record_by_id(db: Session, id: int):
    return db.query(tables.StagingChanges).filter(tables.StagingChanges.id == id).first()


def create_staging_record(db: Session, request: StagingChangeRequest):
    logger.debug("create_staging_record")

    if request.target_id:
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

    # Convert the pydantic model into a standard json string to serialise things like datetime objects
    payload_dict = {}
    for key, value in request.payload.dict().items():
        if isinstance(value, datetime.date):
            value = str(value)
        payload_dict[key] = value
    request.payload = payload_dict

    record = tables.StagingChanges(**request.dict())
    db.add(record)

    try:
        db.commit()
        db.refresh(record)
        return record

    except sqlalchemy.exc.IntegrityError:
        raise backend_api.exc.DuplicateStagingChangePayload


def modify_staging_record(db: Session, request: StagingChangeRequest):
    """
    Request to change the record of an existing entry in a table, by adding an entry to the
    _staging_changes table
    """
    logger.debug(request)

    if request.target_id is None:
        raise AssertionError("target_id is required")

    table_model = get_table_model_by_name(request.target_table)

    # the master record is the existing record that is being requested to change
    master_record_query = db.query(table_model)\
        .filter(table_model.c.id == request.target_id)
    master_record = master_record_query.first()._asdict()

    if master_record is None:
        raise backend_api.exc.MasterRecordNotFoundError

    logger.debug(f"master record:")
    logger.debug(f"{master_record.keys()}")
    logger.debug(type(master_record))

    # check for deltas, as potentially nothing actually changed
    for key, value in request.payload.dict().items():
        logger.debug(f"Checking {key}")
        if master_record.get(key) != value:
            logger.debug(f"Found a delta for {key}. Before: {master_record.get(key)} After: {value}")
            break
    else:
        logger.debug("Request payload is identical to current state. Nothing to do")
        raise backend_api.exc.StagingChangeNoEffectError

    # Convert the pydantic model into a standard json string to serialise things like datetime objects
    payload_dict = {}
    for key, value in request.payload.dict().items():
        if isinstance(value, datetime.date):
            value = str(value)
        payload_dict[key] = value
    request.payload = payload_dict

    # Look for pending (approved = null) records which have a matching target table and id
    staging_record_query = db.query(tables.StagingChanges) \
        .filter(tables.StagingChanges.approved == None) \
        .filter(tables.StagingChanges.target_table == request.target_table) \
        .filter(tables.StagingChanges.target_id == request.target_id)
    staging_record = staging_record_query.first()

    if staging_record:
        logger.debug(f"Staging record exists for id {request.target_id} in {request.target_table}")
        # for key, value in request.dict().items():
        #     logger.debug(f"Updaing {key} with {value}")
        #     staging_record.key = value
        staging_record_query.update({**request.dict()})
        db.commit()
        logger.debug(f"Staging record: {staging_record.__dict__}")
        return staging_record

    staging_record = tables.StagingChanges(**request.dict())

    db.add(staging_record)

    try:
        db.commit()
        return staging_record
    except sqlalchemy.exc.IntegrityError:
        logger.info(f"A StagingChange record already exists with payload ({request.payload})")
        db.rollback()
        return db.query(tables.StagingChanges)\
            .filter(tables.StagingChanges.target_table == request.target_table)\
            .filter(tables.StagingChanges.target_id == request.target_id)\
            .first()


def read_all_staging_records(db: Session, skip: int, limit: int):
    return db.query(tables.StagingChanges).offset(skip).limit(limit).all()


def pending_count(db: Session):
    return db.query(tables.StagingChanges).filter(tables.StagingChanges.approved == None).count()


def get_delta_for_record(db: Session, staging_id: int):
    # get the staging record
    staging_record = db.query(tables.StagingChanges).filter(tables.StagingChanges.id == staging_id).first()

    if not staging_record:
        raise backend_api.exc.StagingRecordNotFoundError

    # Special case for links - should break out into separate functions etc
    if staging_record.target_table.startswith("_association"):
        practice = db.query(tables.Practice).filter(tables.Practice.id == staging_record.target_id).first()
        existing_systems = [system.id for system in practice.access_systems]
        delta = {"before": existing_systems, "after": [x["item"] for x in staging_record.payload["elements"]]}
        return {"deltas": delta}

    # find the table where the master record is
    table_model = get_table_model_by_name(staging_record.target_table)

    if staging_record.target_id is None:
        logger.debug("Staging record has no target id")
        delta = {key: {"before": None, "after": value} for key, value in staging_record.payload.items()}

    else:
        logger.debug(table_model)
        master_record = db.query(table_model).filter(table_model.c.id == staging_record.target_id).first()._asdict()
        delta = {key: {"before": master_record.get(key), "after": value} for key, value in staging_record.payload.items() if master_record.get(key) != value}

    logger.debug(delta)
    return {"deltas": delta}


def approve_staging_change(db: Session, staging_id: int, approver_id: int = 5000):
    """
    Approving means retrieving the staging record, and updating the main record, then marking this as approved.
    """
    # Get the staging record
    staging_record = db.query(tables.StagingChanges).filter(tables.StagingChanges.id == staging_id).first()

    # Update the target table with the new payload
    table = get_table_model_by_name(staging_record.target_table)
    id = staging_record.target_id

    if staging_record.target_table.startswith("_association_practice_systems"):
        practice = db.query(tables.Practice).filter(tables.Practice.id == id).first()
        practice.access_systems = []
        for pair in staging_record.payload["elements"]:
            access_system = db.query(tables.AccessSystem).filter(tables.AccessSystem.id == pair["item"]).first()
            practice.access_systems.append(access_system)

    else:
        if id is None:
            # Create a new record
            statement = table.insert().values(**staging_record.payload)
        else:
            statement = table.update().where(table.c.id == id).values(**staging_record.payload)
        logger.debug(statement)
        db.execute(statement)

    db.commit()

    # Mark as approved in the staging changes table
    staging_record.approved = True
    staging_record.approver_id = approver_id
    db.commit()
    return staging_record


def reject_staging_change(db: Session, staging_id: int, approver_id: int = 5000):
    staging_record = db.query(tables.StagingChanges).filter(tables.StagingChanges.id == staging_id).first()
    staging_record.approved = False
    staging_record.approver_id = approver_id
    db.commit()
    return staging_record


def modify_staging_record_m2m(db: Session, request: StagingChangeRequest):
    logger.debug(request)
    if request.target_table == "_association_practice_systems":

        # Check for existing pending record
        query = db.query(tables.StagingChanges)\
            .filter(tables.StagingChanges.approved == None)\
            .filter(tables.StagingChanges.target_table == request.target_table)\
            .filter(tables.StagingChanges.target_id == request.target_id)\
            .filter(tables.StagingChanges.link == True)

        if query.first():
            # Check if the existing pending record payload is already the same as the new request payload
            if query.first().payload == request.payload:
                logger.debug("Nothing to do to modify m2m record")
                return query.first()

        # Check if the new request payload actually is the current state

        # If we pass the above checks, then we either need to update the payload of the existing request
        if query.first():
            logger.debug("Updating existing staging record")
            query.update({**request.dict()})
            db.commit()
            return query.first()

        # Or create a new one for it
        staging_record = tables.StagingChanges(**request.dict())
        db.add(staging_record)
        db.commit()
        return staging_record

        # if request.payload.action == "add":
        #     for element in request.payload.elements:
        #         access_system = db.query(tables.AccessSystem).filter(tables.AccessSystem.id == element).first()
        #         practice.access_systems.append(access_system)