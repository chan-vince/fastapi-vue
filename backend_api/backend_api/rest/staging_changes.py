import logging
from typing import List, Union

from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import backend_api.pydantic_schemas as schemas
import backend_api.exc
# from backend_api.crud.staging_changes import *
from backend_api.database import get_db, table_names, printable_tables

logger = logging.getLogger("REST:StagingEmployees")

# Create a fastapi router for these REST endpoints
router = APIRouter()


@router.put("/ip_range", response_model=schemas.StagingChangeResponse)
def change_existing_ip_range(request: schemas.StagingChangeRequest, db: Session = Depends(get_db)):
    """
    Modify an existing IP Range
    :param request: the request body must contain the keys defined in the StagingChangeRequest schema
    :param db:
    :return: schemas.StagingChangeResponse
    """

    # Ensure the target table exists
    if request.target_table not in table_names:
        raise HTTPException(status_code=400, detail=f"Invalid target_table, must be one of {printable_tables}")

    # Ensure that target_id is not set if the modify flag is false
    if not request.modify and request.target_id is not None:
        raise HTTPException(status_code=400, detail=f"Do not specify a target_id if you intend to create a new entry")

    # # If the modify flag is true, then an existing record must exist
    # if request.modify and not id_exists(db, request.target_table, request.target_id):
    #     raise HTTPException(status_code=400, detail=f"No record in {request.target_table} with ID {request.target_id}")

    return None
