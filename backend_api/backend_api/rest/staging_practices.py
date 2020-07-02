import logging
from typing import List, Union

from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import backend_api.pydantic_schemas as schemas
from backend_api.crud import practices as crud_practices
from backend_api.crud import staging_practices as crud_staging_practices
from backend_api.database import get_db

logger = logging.getLogger("REST:Practices")

# Create a fastapi router for these REST endpoints
router = APIRouter()


@router.put("/practice", response_model=schemas.StagingRequest)
def modify_practice_details(changed_practice: schemas.StagingPracticeRequest, db: Session = Depends(get_db)):
    practice = crud_practices.read_practice_by_id(db, changed_practice.source_id)
    if practice is None:
        raise HTTPException(status_code=404, detail=f"GP Practice with ID {changed_practice.source_id} doesn't exist")

    return crud_staging_practices.update_staging_practice(db, changed_practice)


@router.get("/practice", response_model=List[schemas.StagingRequest])
def get_all_staging_practices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_staging_practices.read_all_staging_practices(db, skip=skip, limit=limit)


@router.get("/practice/count/pending")
def get_staging_practice_count(db: Session = Depends(get_db)):
    return crud_staging_practices.read_staging_practices_count_pending(db)


@router.put("/practice/approved", response_model=schemas.StagingRequest)
def action_staging_practice_changes(id: int, approved: Union[bool, None], db: Session = Depends(get_db)):
    return crud_staging_practices.action_pending_changes_to_practice_by_id(db, id, approved)
