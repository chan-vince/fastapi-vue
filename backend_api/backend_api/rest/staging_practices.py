import logging
from typing import List

from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import backend_api.pydantic_schemas as schemas
from backend_api.crud import practices as crud_practices
from backend_api.crud import staging_practices as crud__staging_practices
from backend_api.database import get_db

logger = logging.getLogger("REST:Practices")

# Create a fastapi router for these REST endpoints
router = APIRouter()


@router.put("/practice/", response_model=schemas.StagingRequest)
def modify_practice_details(changed_practice: schemas.StagingPracticeRequest, db: Session = Depends(get_db)):
    practice = crud_practices.read_practice_by_id(db, changed_practice.source_id)
    if practice is None:
        raise HTTPException(status_code=404, detail=f"GP Practice with ID {changed_practice.source_id} doesn't exist")

    return crud__staging_practices.update_staging_practice(db, changed_practice)
