import json

import sqlalchemy.exc
from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import backend_api.database
import backend_api.database
import backend_api.database_models as tables
import backend_api.exc
import backend_api.pydantic_schemas as schemas
from backend_api.database_connection import get_db_session
from backend_api.utils import get_pydantic_model_for_entity, get_sqlalchemy_model_for_entity, columns_to_dict
from ..log_setup import logger

# Create a fastapi router for these REST endpoints
router = APIRouter()


@router.get("/changes/pending/all")
def get_all_pending_requests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)):
    return backend_api.database.read_all_pending_change_requests(db, skip, limit)


@router.get("/changes/pending/count")
def get_all_pending_requests(db: Session = Depends(get_db_session)):
    return backend_api.database.read_all_pending_change_requests_count(db)


@router.get("/changes/history/all")
def get_all_historic_requests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)):
    return backend_api.database.read_all_historic_change_requests(db, skip, limit)


@router.get("/changes/history/id")
def get_change_history_for_existing_record(target_name: str, target_id: int, db: Session = Depends(get_db_session)):
    table = get_sqlalchemy_model_for_entity(target_name)
    if table is None:
        raise HTTPException(status_code=422, detail=f"Unknown target_name {target_name}")

    existing_record = backend_api.database.read_existing_record_by_id(db, target_id, table)
    if not existing_record:
        raise HTTPException(status_code=404, detail=f"No record found of type {target_name} with id {target_id}")

    history = backend_api.database.read_all_historic_change_requests_for_target(db, target_name, target_id)

    return {"current": existing_record, "history": history}


@router.post("/change/request")
def submit_new_change_request(request: schemas.ChangeRequest, db: Session = Depends(get_db_session)):
    """
    This is also for creating 'new' objects - adding an object is kind of changing the state of the system?
    """
    # Check for a duplicate
    identical_pending_record = backend_api.database.read_pending_change_requests_with_matching_new_state(db, request)
    if identical_pending_record is not None:
        return identical_pending_record

    # Request to add a new thing
    if request.target_id is None:
        # Note: pydantic handles the validation of target_name
        logger.debug(f"New change request: {request}")
        logger.debug(f"Request name: {request.target_name}\t"
                     f"Request schema: {get_pydantic_model_for_entity(request.target_name)}")

        # Create the change request. The new_state dict is automagically validated with pydantic already
        return backend_api.database.create_change_request(db, request.dict())

    # Requst to modify an existing thing
    else:
        # find the existing record
        table = get_sqlalchemy_model_for_entity(request.target_name)

        # use the table and target_id to find the record to change
        existing_record = backend_api.database.read_existing_record_by_id(db, request.target_id, table)

        # if the record doesn't exist then we can't change it
        if existing_record is None:
            raise HTTPException(status_code=404, detail=f"No existing {request.target_name} entry with target_id {request.target_id}")

        # Since there should only be one pending request per row, check the ChangeHistory for pending with the same
        # target table and id
        existing_pending_record = backend_api.database.read_pending_change_requests_with_matching_target(db, request)
        if existing_pending_record:
            return backend_api.database.update_change_request_new_state(db, request.new_state.dict(), existing_pending_record)

        # serialise using json to sort keys and stringify by default to eat up the datetime objects
        current_state = json.loads(json.dumps(columns_to_dict(existing_record), sort_keys=True, default=str))
        logger.debug(f"is there the stuff: {current_state}")
        logger.debug(f"Update change request for existing record: {current_state}")

        return backend_api.database.create_change_request(db, request.dict(), current_state=current_state)


@router.put("/change/request/approve", response_model=schemas.ChangeResponse)
def approve_change_request(change_request_id: int, db: Session = Depends(get_db_session)):
    """
    Once a user system has been implemented, this should be a protected route to only allow certain users to
    approve a request
    """
    record: tables.ChangeHistory = backend_api.database.read_change_request(db, change_request_id)

    if record.approval_status is True:
        logger.debug(f"Already approved, nothing to do")
        return record

    if record is None:
        raise HTTPException(status_code=404, detail=f"No change request found with id {change_request_id}")

    table = get_sqlalchemy_model_for_entity(record.target_name)
    try:
        existing_record = backend_api.database.update_existing_record_by_id(db, record.target_id, table, record.new_state)
    except sqlalchemy.exc.IntegrityError as e:
        raise HTTPException(status_code=422, detail=f"{e}")

    if existing_record:
        logger.debug(f"Updated entry: {columns_to_dict(existing_record)}")

    # Create a new object and write to db
    if existing_record is None:
        new_entry = backend_api.database.create_entry_in_table(db,
                                                               get_sqlalchemy_model_for_entity(record.target_name),
                                                               record.new_state)
        logger.debug(f"New entry: {columns_to_dict(new_entry)}")

    # do a hardcoded approver id for now since we don't have admins
    record.approver_id = 1
    record.approval_status = True
    db.commit()

    logger.debug("Record approved and updated")

    return record


@router.put("/change/request/reject")
def reject_change_request(change_request_id: int, db: Session = Depends(get_db_session)):
    """
    Once a user system has been implemented, this should be a protected route to only allow certain users to
    reject a request
    """
    record: tables.ChangeHistory = backend_api.database.read_change_request(db, change_request_id)

    if record is None:
        raise HTTPException(status_code=404, detail=f"No change request found with id {change_request_id}")

    record.approver_id = 1
    record.approval_status = False
    db.commit()
    logger.debug("Record change rejected")
    return record
