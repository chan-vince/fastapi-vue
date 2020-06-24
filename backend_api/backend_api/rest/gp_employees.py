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
        raise HTTPException(status_code=400, detail=f"GP Employee with email {new_gp_employee.email} already registered")
    return crud.add_gp_employee(db, new_gp_employee)


@router.get("/gp_employee/id/", response_model=schemas.GPEmployee)
def get_gp_employee_by_id(gp_employee_id: int, db: Session = Depends(get_db)):
    # todo
    pass


@router.get("/gp_employee/email/", response_model=schemas.GPEmployee)
def get_gp_employee_by_email(email: str, db: Session = Depends(get_db)):
    # todo
    pass


@router.get("/gp_employee/professional_num/", response_model=schemas.GPEmployee)
def get_gp_employee_by_professional_num(professional_num: str, db: Session = Depends(get_db)):
    # todo
    pass