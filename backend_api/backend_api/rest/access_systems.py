import logging
from typing import List

from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import backend_api.pydantic_schemas as schemas
from backend_api import database
from backend_api.database_connection import get_db_session

logger = logging.getLogger("REST:Practices")

# Create a fastapi router for these REST endpoints
router = APIRouter()


@router.get("/access_system/all", response_model=List[schemas.AccessSystem])
def get_all_access_systems(db: Session = Depends(get_db_session)):
    return database.get_all_access_systems(db)


@router.get("/access_system/id", response_model=schemas.AccessSystem)
def get_access_system_by_id(access_system_id: int, db: Session = Depends(get_db_session)):
    return database.get_access_system_by_id(db, access_system_id)


@router.get("/access_system/name", response_model=schemas.AccessSystem)
def get_access_system_by_name(name: str, db: Session = Depends(get_db_session)):
    access_system = database.get_access_system_by_name(db, name)

    if access_system is None:
        raise HTTPException(status_code=404, detail=f"No access system found with name '{name}'")

    return access_system


# @router.post("/access_system", response_model=schemas.AccessSystem)
# def create_new_access_system(access_system: schemas.AccessSystemCreate, db: Session = Depends(get_db_session)):
#     return database.add_access_system(db, access_system)


# @router.delete("/access_system", response_model=schemas.AccessSystem)
# def delete_access_system(access_system_id: int, db: Session = Depends(get_db_session)):
#     return database.delete_access_system(db, access_system_id)
