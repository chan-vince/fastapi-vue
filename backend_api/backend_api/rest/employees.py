from typing import List

from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import backend_api.pydantic_schemas as schemas
from backend_api import database
from backend_api.database_connection import get_db_session

# Create a fastapi router for these REST endpoints
router = APIRouter()


@router.get("/employee/all", response_model=List[schemas.Employee])
def get_all_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)):
    employees = database.read_all_employees(db, skip=skip, limit=limit)
    return employees


@router.get("/employee/id", response_model=schemas.Employee)
def get_employee_by_id(employee_id: int, db: Session = Depends(get_db_session)):
    employee = database.read_employee_by_id(db, employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail=f"No employee found with ID {employee_id}")
    return employee


@router.get("/employee/name", response_model=schemas.Employee)
def get_employee_by_name(name: str, db: Session = Depends(get_db_session)):
    employee = database.read_employee_by_name(db, name)
    if employee is None:
        raise HTTPException(status_code=404, detail=f"No employee found with first name {name}")
    return employee


@router.get("/employee/email", response_model=schemas.Employee)
def get_employee_by_email(email: str, db: Session = Depends(get_db_session)):
    employee = database.read_employee_by_email(db, email)
    if employee is None:
        raise HTTPException(status_code=404, detail=f"No employee found with email {email}")
    return employee


@router.get("/employee/professional_num", response_model=schemas.Employee)
def get_employee_by_professional_num(professional_num: str, db: Session = Depends(get_db_session)):
    employee = database.read_employee_by_professional_num(db, professional_num)
    if employee is None:
        raise HTTPException(status_code=404, detail=f"No employee found with professional num {professional_num}")
    return employee


@router.get("/employee/count", response_model=schemas.RowCount)
def get_total_number_employees(db: Session = Depends(get_db_session)):
    return schemas.RowCount(count=database.read_total_number_of_employees(db))


@router.get("/employee/names", response_model=schemas.EntityNames)
def get_names_of_employees(db: Session = Depends(get_db_session)):
    return schemas.EntityNames(names=database.read_all_employee_names(db))
