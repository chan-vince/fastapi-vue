from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import backend_api.pydantic_schemas as schemas
from backend_api import crud
from backend_api.database import get_db

# Create a fastapi router for these REST endpoints
router = APIRouter()


@router.post("/employee/", response_model=schemas.Employee)
def add_new_employee(new_employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    employee = crud.get_employee_by_email(db, new_employee.email)
    if employee:
        raise HTTPException(status_code=400, detail=f"GP Employee with email {new_employee.email} already registered")
    return crud.add_employee(db, new_employee)


@router.get("/employee/id/", response_model=schemas.Employee)
def get_employee_by_id(employee_id: int, db: Session = Depends(get_db)):
    # todo
    pass


@router.get("/employee/email/", response_model=schemas.Employee)
def get_employee_by_email(email: str, db: Session = Depends(get_db)):
    # todo
    pass


@router.get("/employee/professional_num/", response_model=schemas.Employee)
def get_employee_by_professional_num(professional_num: str, db: Session = Depends(get_db)):
    # todo
    pass