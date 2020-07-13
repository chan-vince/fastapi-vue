import logging
from typing import List, Union, Any

from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import backend_api.pydantic_schemas as schemas
import backend_api.exc
from backend_api.crud.staging_changes import id_exists
from backend_api.database import get_db, table_names, printable_tables
from backend_api.crud import staging_changes as crud

logger = logging.getLogger("REST:StagingChanges")

# Create a fastapi router for these REST endpoints
router = APIRouter()


@router.get("/stagingbeta/id", response_model=schemas.StagingChangeResponse)
def get_staging_record_by_id(id: int, db: Session = Depends(get_db)):
    result = crud.read_staging_record_by_id(db, id)
    if result is None:
        raise HTTPException(status_code=404)
    else:
        return result


@router.post("/stagingbeta", response_model=schemas.StagingChangeResponse)
def create_new_record_request(request: schemas.StagingChangeRequest, db: Session = Depends(get_db)):
    """
    Stores a record in the staging changes table, which details which table to put this new payload in. Don't forget
    the "payload" object, which for some reason is broken if you're viewing this from the docs page
    """

    # Ensure the target table exists
    if request.target_table not in table_names:
        raise HTTPException(status_code=400, detail=f"Invalid target_table, must be one of {printable_tables}")

    # Ensure that target_id is not set since we're not modifying
    if request.modify or request.target_id is not None:
        raise HTTPException(status_code=400, detail=f"target_id is set or modify is true. Use the PUT request to modify an existing entry")

    # # # If the modify flag is true, then an existing record must exist
    # if request.modify and not id_exists(db, request.target_table, request.target_id):
    #     raise HTTPException(status_code=400, detail=f"No record in {request.target_table} with ID {request.target_id}")

    try:
        record = crud.create_staging_record(db, request)
        return record

    except AssertionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except backend_api.exc.DuplicateStagingChangePayload:
        raise HTTPException(status_code=409, detail=f"A request already exists with payload: {request.payload}")


@router.get("/stagingbeta/delta", response_model=schemas.StagingChangeDeltaResponse)
def get_delta_between_current_record_and_change_request(id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_delta_for_record(db, id)
    except backend_api.exc.StagingRecordNotFoundError:
        raise HTTPException(status_code=404)


@router.put("/stagingbeta", response_model=Union[schemas.StagingChangeResponse, Any])
def modify_existing_record_request(request: schemas.StagingChangeRequest, db: Session = Depends(get_db)):

    # Ensure the target table exists
    if request.target_table not in table_names:
        raise HTTPException(status_code=400, detail=f"Invalid target_table, must be one of {printable_tables}")

    # Ensure the right parameters are set
    if not request.modify or request.target_id is None:
        raise HTTPException(status_code=400, detail=f"To modify a request, set modify to true and set target_id to a row id")

    try:
        return crud.modify_staging_record(db, request)
    except AssertionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except backend_api.exc.MasterRecordNotFoundError:
        raise HTTPException(status_code=409, detail=f"No entry exists with id {request.target_id} in table {request.target_table}")
    except backend_api.exc.StagingChangeNoEffectError:
        return HTTPException(status_code=204)


@router.get("/stagingbeta", response_model=List[schemas.StagingChangeResponse])
def get_all_staging_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.read_all_staging_records(db, skip=skip, limit=limit)


@router.put("/stagingbeta/approve", response_model=schemas.StagingChangeResponse)
def approve_pending_staging_request(staging_id: int, approver_id: int, db: Session = Depends(get_db)):
    return crud.approve_staging_change(db, staging_id, approver_id)


@router.put("/stagingbeta/reject", response_model=schemas.StagingChangeResponse)
def reject_pending_staging_request(staging_id: int, approver_id: int, db: Session = Depends(get_db)):
    return crud.reject_staging_change(db, staging_id, approver_id)


@router.get("/stagingbeta/count/pending")
def get_pending_count(db: Session = Depends(get_db)):
    return crud.pending_count(db)