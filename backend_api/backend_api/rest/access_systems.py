import logging
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List

import backend_api.pydantic_schemas as schemas
from backend_api.crud import practices as crud_practices
from backend_api.database import get_db

logger = logging.getLogger("REST:Practices")

# Create a fastapi router for these REST endpoints
router = APIRouter()


@router.get("/access_system", response_model=List[schemas.AccessSystem])
def get_all_access_systems(db: Session = Depends(get_db)):
    return crud_practices.get_all_access_systems(db)


@router.get("/access_system/{access_system_id}", response_model=schemas.AccessSystem)
def get_access_system_by_id(access_system_id: int, db: Session = Depends(get_db)):
    return crud_practices.get_access_system_by_id(db, access_system_id)


@router.post("/access_system", response_model=schemas.AccessSystem)
def create_new_access_system(access_system: schemas.AccessSystemCreate, db: Session = Depends(get_db)):
    return crud_practices.add_access_system(db, access_system)


@router.delete("/access_system", response_model=schemas.AccessSystem)
def delete_access_system(access_system_id: int, db: Session = Depends(get_db)):
    return crud_practices.delete_access_system(db, access_system_id)
