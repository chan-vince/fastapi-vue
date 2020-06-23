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


@router.get("/gp_practice/{gp_practice_id}", response_model=schemas.GPPractice)
def read_gp_practice(gp_practice_id: int, db: Session = Depends(get_db)):
    gp_practice = crud.get_gp_practice_by_id(db, gp_practice_id=gp_practice_id)
    if gp_practice is None:
        raise HTTPException(status_code=404, detail=f"GP Practice with id {gp_practice_id} not found")
    return gp_practice


@router.post("/gp_practice/", response_model=schemas.GPPractice)
def add_new_gp_practice(gp_practice: schemas.GPPracticeCreate, db: Session = Depends(get_db)):
    gp_practice = crud.get_gp_practice_by_name_ice(db, gp_practice.name_ice)
    if gp_practice:
        raise HTTPException(status_code=400, detail=f"GP Practice with name {gp_practice.name_ice} already registered")
    return crud.create_gp_practice(db=db, gp_practice=gp_practice)

