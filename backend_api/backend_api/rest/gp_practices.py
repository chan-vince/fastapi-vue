from typing import List

from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import backend_api.pydantic_schemas as schemas
from backend_api import crud
from backend_api.database import get_db

# logger = logging.getLogger("REST:GPPractices")
# logging.basicConfig(
#     format="%(asctime)s: %(levelname)s: %(name)s - %(message)s", level=get_config()['General']['LogLevel']
# )

# Create a fastapi router for these REST endpoints
router = APIRouter()


@router.post("/gp_practice/", response_model=schemas.GPPractice)
def add_update_new_gp_practice(gp_practice: schemas.GPPracticeCreate, db: Session = Depends(get_db)):
    gp_practice = crud.get_gp_practice_by_name(db, gp_practice.name)
    if gp_practice:
        raise HTTPException(status_code=400, detail=f"GP Practice with name {gp_practice.name} already registered")
    return crud.update_gp_practice(db=db, updated_gp_practice=gp_practice)


@router.post("/gp_practice/{gp_practice_id}/address", response_model=schemas.GPAddress)
def add_update_address_for_gp_practice_by_id(gp_practice_id: int,
                                             new_address: schemas.GPAddressCreate,
                                             db: Session = Depends(get_db)):

    gp_practice = read_gp_practice_by_id(gp_practice_id=gp_practice_id, db=db)
    if gp_practice is None:
        raise HTTPException(status_code=404, detail=f"No GP Practice with id {gp_practice_id}")

    return crud.update_gp_address_by_gp_practice_id(db, gp_practice_id=gp_practice_id, new_address=new_address)


@router.get("/gp_practice/", response_model=List[schemas.GPPractice])
def read_all_gp_practices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    gp_practices = crud.get_gp_practices_all(db, skip=skip, limit=limit)
    return gp_practices


@router.get("/gp_practice/id/", response_model=schemas.GPPractice)
def read_gp_practice_by_id(gp_practice_id: int, db: Session = Depends(get_db)):
    gp_practice: schemas.GPPractice = crud.get_gp_practice_by_id(db, gp_practice_id=gp_practice_id)
    if gp_practice is None:
        raise HTTPException(status_code=404, detail=f"GP Practice with id {gp_practice_id} not found")
    return gp_practice


@router.get("/gp_practice/name/", response_model=schemas.GPPractice)
def read_gp_practice_by_name(name: str, db: Session = Depends(get_db)):
    gp_practice: schemas.GPPractice = crud.get_gp_practice_by_name(db, gp_name=name)
    if gp_practice is None:
        raise HTTPException(status_code=404, detail=f"GP Practice with name {name} not found")
    return gp_practice


@router.get("/gp_practice/address/", response_model=schemas.GPAddress)
def read_gp_practice_address_by_name(name: str, db: Session = Depends(get_db)):
    if crud.get_gp_practice_by_name(db, name) is None:
        raise HTTPException(status_code=400, detail=f"No GP Practice with name {name}")

    gp_address: schemas.GPAddress = crud.get_gp_address_by_gp_practice_name(db, gp_practice_name=name)
    if gp_address is None:
        raise HTTPException(status_code=404, detail=f"No address for GP Practice with name {name}")
    return gp_address
