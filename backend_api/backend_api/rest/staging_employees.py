import logging
from typing import List, Union

from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import backend_api.pydantic_schemas as schemas
from backend_api.crud import employees as crud_employees
from backend_api.crud import staging_employees as crud_staging_employees
from backend_api.database import get_db

logger = logging.getLogger("REST:StagingEmployees")

# Create a fastapi router for these REST endpoints
router = APIRouter()


@router.post("/employee", response_model=schemas.StagingEmployeeRequest)
def submit_request_to_add_employee(new_employee: schemas.StagingEmployeeCreateRequest, db: Session = Depends(get_db)):
    return crud_staging_employees.add_new_staging_employee(db, new_employee)


@router.put("/employee", response_model=schemas.StagingEmployeeRequest)
def modify_employee_details(changed_employee: schemas.StagingEmployeeCreateRequest, db: Session = Depends(get_db)):
    employee = crud_employees.read_employee_by_id(db, changed_employee.source_id)
    if employee is None:
        raise HTTPException(status_code=404, detail=f"GP employee with ID {changed_employee.source_id} doesn't exist")

    thing = crud_staging_employees.update_staging_employee(db, changed_employee)
    print(thing)
    return thing


@router.get("/employee", response_model=List[schemas.StagingEmployeeRequest])
def get_all_staging_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_staging_employees.read_all_staging_employees(db, skip=skip, limit=limit)


@router.get("/employee/count/pending")
def get_staging_employee_count(db: Session = Depends(get_db)):
    return crud_staging_employees.read_staging_employees_count_pending(db)


@router.put("/employee/approved", response_model=schemas.StagingEmployeeRequest)
def action_staging_employee_changes(id: int, approved: Union[bool, None], db: Session = Depends(get_db)):
    return crud_staging_employees.action_pending_changes_to_employee_by_id(db, id, approved)
