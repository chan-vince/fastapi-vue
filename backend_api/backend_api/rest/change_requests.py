import json
from typing import List

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


@router.get("/changes/pending/all", response_model=List[schemas.ChangeResponse])
def get_all_pending_requests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)):
    return backend_api.database.read_all_pending_change_requests(db, skip, limit)


@router.get("/changes/pending/count")
def get_all_pending_requests(db: Session = Depends(get_db_session)):
    return backend_api.database.read_all_pending_change_requests_count(db)


@router.get("/changes/pending/id")
def get_pending_request_by_id(id: int, db: Session = Depends(get_db_session)):
    return backend_api.database.read_change_request(db, id)


@router.get("/changes/pending/id/delta")
def get_delta_for_pending_request_by_id(id: int, db: Session = Depends(get_db_session)):
    change_request: schemas.ChangeRequest = backend_api.database.read_change_request(db, id)

    if change_request is None:
        raise HTTPException(status_code=404, detail=f"No change request with ID {id}")

    # The parent is the table, the child is the column
    if "." in change_request.target_name:
        parent, child = tuple(change_request.target_name.split('.'))

        # get the record specified by the table/id combo
        record = backend_api.database.read_existing_record_by_id(db,
                                                                 change_request.target_id,
                                                                 get_sqlalchemy_model_for_entity(parent))
        # the before state is simply the current value
        before = getattr(record, child)
        return {
            "before": before,
            "after": change_request.new_state.get('data')
        }

    # If it's just an object directly from the table, we can directly use the current_state as the before state
    else:
        before: dict = change_request.current_state
        if change_request.target_name == "employee":
            # get the record specified by the table/id combo
            record: tables.Employee = backend_api.database.read_existing_record_by_id(db,
                                                                     change_request.target_id,
                                                                     tables.Employee)
            before["practice_ids"] = [practice.id for practice in record.practices]

    # The delta includes before/after for each attribute column of the object if there's a difference
    delta = {
        key: {
            "before": before.get(key),
            "after": value
        }
        for key, value in change_request.new_state.items()
        if before.get(key) != value}

    return delta


@router.get("/changes/history/all", response_model=List[schemas.ChangeResponse])
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

    if "." in request.target_name:
        parent, child = tuple(request.target_name.split('.'))
    else:
        parent = request.target_name

    # Request to add a new thing
    if request.target_id is None:
        # Note: pydantic handles the validation of target_name
        logger.debug(f"New change request: {request}")
        logger.debug(f"Request name: {parent}\t"
                     f"Request schema: {get_pydantic_model_for_entity(parent)}")

        # Create the change request. The new_state dict is automagically validated with pydantic already
        return backend_api.database.create_change_request(db, request.dict())

    # Requst to modify an existing thing
    else:
        # find the existing record
        table = get_sqlalchemy_model_for_entity(parent)
        logger.debug(f"!!!!{parent}")
        logger.debug(f"!!!!{table}")

        # use the table and target_id to find the record to change
        existing_record = backend_api.database.read_existing_record_by_id(db, request.target_id, table)

        # if the record doesn't exist then we can't change it
        if existing_record is None:
            raise HTTPException(status_code=404, detail=f"No existing {parent} entry with target_id {request.target_id}")

        # Since there should only be one pending request per row, check the ChangeHistory for pending with the same
        # target table and id
        existing_pending_record = backend_api.database.read_pending_change_requests_with_matching_target(db, request)
        if existing_pending_record:
            return backend_api.database.update_change_request_new_state(db, request.new_state.dict(), existing_pending_record)

        # serialise using json to sort keys and stringify by default to eat up the datetime objects. should switch this
        #  to pydantic's built in .json() method which can handle datetimes
        current_state = json.loads(json.dumps(columns_to_dict(existing_record), sort_keys=True, default=str))
        request.current_state = current_state
        logger.debug(f"Update change request for existing record: {current_state}")
        return backend_api.database.create_change_request(db, request.dict())


@router.put("/change/request/approve", response_model=schemas.ChangeResponse)
def approve_change_request(change_request_id: int, approver_id: int = 1, db: Session = Depends(get_db_session)):
    """
    Once a user system has been implemented, this should be a protected route to only allow certain users to
    approve a request
    """
    change_request: tables.ChangeHistory = backend_api.database.read_change_request(db, change_request_id)

    if change_request.approval_status is True:
        logger.debug(f"Already approved, nothing to do")
        return change_request

    if change_request is None:
        raise HTTPException(status_code=404, detail=f"No change request found with id {change_request_id}")

    if "." in change_request.target_name:
        parent, child = tuple(change_request.target_name.split('.'))
    else:
        parent = change_request.target_name
        child = None

    table = get_sqlalchemy_model_for_entity(parent)

    if "." in change_request.target_name:
        record = backend_api.database.read_existing_record_by_id(db,
                                                                 change_request.target_id,
                                                                 get_sqlalchemy_model_for_entity(parent))

        if change_request.new_state.get("action") == "replace":
            setattr(record, child, [backend_api.database.read_existing_record_by_id(db, element["id"], get_sqlalchemy_model_for_entity(child)) for element in change_request.new_state.get("data")])
            logger.debug(record.access_systems)
            db.commit()

    else:
        new_state: dict = change_request.new_state
        practice_ids = new_state.pop("practice_ids", None)
        try:
            existing_record = backend_api.database.update_existing_record_by_id(db,
                                                                                change_request.target_id,
                                                                                table,
                                                                                new_state)
        except sqlalchemy.exc.IntegrityError as e:
            raise HTTPException(status_code=422, detail=f"{e}")

        if existing_record:
            logger.debug(f"Updated entry: {existing_record}")

        # Create a new object and write to db
        if existing_record is None:
            new_entry: tables.Employee = backend_api.database.create_entry_in_table(db,
                                                                                    get_sqlalchemy_model_for_entity(parent),
                                                                                    new_state)
            logger.debug(f"New entry: {new_entry}")

        # Do the practice assignment if the request is a employee
        if parent == "employee" and practice_ids is not None:
            for practice_id in practice_ids:
                logger.info(f"Linking employee {change_request.target_id} to practice {practice_id}")
                backend_api.database.unassign_employee_from_all_practices(db, change_request.target_id)
                backend_api.database.assign_employee_to_practice(db, change_request.target_id, practice_id)

    # do a hardcoded approver id for now since we don't have admins
    change_request.approver_id = approver_id
    change_request.approval_status = True
    db.commit()

    logger.debug("Record approved and updated")

    return change_request


@router.put("/change/request/reject")
def reject_change_request(change_request_id: int, approver_id: int = 1, db: Session = Depends(get_db_session)):
    """
    Once a user system has been implemented, this should be a protected route to only allow certain users to
    reject a request
    """
    record: tables.ChangeHistory = backend_api.database.read_change_request(db, change_request_id)

    if record is None:
        raise HTTPException(status_code=404, detail=f"No change request found with id {change_request_id}")

    record.approver_id = approver_id
    record.approval_status = False
    db.commit()
    logger.debug("Record change rejected")
    return record
