import logging
from typing import List, Union

from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import backend_api.pydantic_schemas as schemas
import backend_api.exc
from backend_api.crud.staging_changes import id_exists
from backend_api.database import get_db, table_names, printable_tables
from backend_api.crud import staging_changes as crud

logger = logging.getLogger("REST:StagingEmployees")

# Create a fastapi router for these REST endpoints
router = APIRouter()


@router.post("/", response_model=schemas.StagingChangeResponse)
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


@router.put("/", response_model=Union[schemas.StagingChangeResponse, None])
def modify_existing_record_request(request: schemas.StagingChangeRequest, db: Session = Depends(get_db)):

    # Ensure the target table exists
    if request.target_table not in table_names:
        raise HTTPException(status_code=400, detail=f"Invalid target_table, must be one of {printable_tables}")

    # Ensure the right parameters are set
    if not request.modify or request.target_id is None:
        raise HTTPException(status_code=400, detail=f"To modify a request, set modify to true and set target_id to a row id")

    return crud.modify_staging_record(db, request)
    try:
        return crud.modify_staging_record(db, request)
    except AssertionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except backend_api.exc.StagingChangeNotFoundError:
        raise HTTPException(status_code=409, detail=f"No entry exists with id {request.target_id} in table {request.target_table}")
    # except backend_api.exc.StagingChangeNoEffectError as e:
        # return HTTPException(status_code=218, detail=e.args[0])


@router.get("/", response_model=List[schemas.StagingChangeResponse])
def get_all_staging_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.read_all_staging_records(db, skip=skip, limit=limit)


@router.get("/delta", response_model=schemas.StagingChangeDeltaResponse)
def get_delta_between_current_record_and_change_request(id: int):
    pass