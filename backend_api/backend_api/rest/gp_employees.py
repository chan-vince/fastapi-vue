from typing import List

from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import backend_api.pydantic_schemas as schemas
from backend_api import crud
from backend_api.database import get_db


# Create a fastapi router for these REST endpoints
router = APIRouter()


@router.post("/gp_employee/", response_model=schemas.GPEmployee)
def add_new_gp_employee(new_gp_employee: schemas.GPEmployeeCreate, db: Session = Depends(get_db)):
    gp_employee = crud.get_gp_employee_by_email(db, new_gp_employee.email)
    if gp_employee:
        raise HTTPException(status_code=400, detail=f"GP Employee with name {new_gp_employee.first_name} already registered")
    return crud.add_gp_employee(db, new_gp_employee)
