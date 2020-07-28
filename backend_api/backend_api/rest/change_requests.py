import json

from ..log_setup import logger
from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Union, Any
from sqlalchemy.orm.collections import InstrumentedList

import backend_api.database

import backend_api.exc
import backend_api.pydantic_schemas as schemas
import backend_api.database_models as tables
from backend_api.database_connection import get_db_session
from backend_api.utils import get_pydantic_model_for_entity, get_sqlalchemy_model_for_entity, columns_to_dict
import backend_api.database

# Create a fastapi router for these REST endpoints
router = APIRouter()


@router.get("/changes/pending/all")
def get_all_pending_requests():
    pass


@router.get("/changes/history/all")
def get_all_historic_requests():
    pass


@router.get("/changes/history/id")
def get_change_history_for_existing_record():
    pass


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

        # # Convert the existing record model into a dict so we can serialise to JSON and store it as the current state
        # current_state = columns_to_dict(existing_record)
        #
        # # Go through the relationships and serialise them too
        # for key, value in current_state.items():
        #     if isinstance(value, InstrumentedList):
        #         current_state[key] = [columns_to_dict(model) for model in value]

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
    existing_record = backend_api.database.update_existing_record_by_id(db, record.target_id, table, record.new_state)

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
