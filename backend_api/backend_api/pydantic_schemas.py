import datetime
from pydantic import BaseModel, Json
from typing import List, Any, Union


class IPRangeBase(BaseModel):
    cidr: str
    address_id: int


class IPRangeCreate(IPRangeBase):
    pass


class IPRange(IPRangeBase):
    id: int

    class Config:
        orm_mode = True


class AddressBase(BaseModel):
    line_1: str
    line_2: Union[str, None]
    town: str
    county: str
    postcode: str
    phone_num: str
    dts_email: str


class AddressCreate(AddressBase):
    pass


class Address(AddressBase):
    id: int
    practice_id: Union[int, None]
    ip_ranges: List[IPRange] = []

    class Config:
        orm_mode = True


class AccessSystemBase(BaseModel):
    name: str


class AccessSystemCreate(AccessSystemBase):
    pass


class AccessSystem(AccessSystemBase):
    id: int

    class Config:
        orm_mode = True


class Association(BaseModel):
    action: str
    elements: List[dict]

    class Config:
        orm_mode = True


class JobTitleBase(BaseModel):
    title: str


class JobTitleCreate(JobTitleBase):
    pass


class JobTitle(JobTitleBase):
    id: int

    class Config:
        orm_mode = True


class PracticeBase(BaseModel):
    name: str
    national_code: str
    emis_cdb_practice_code: str
    go_live_date: str
    closed: bool


class PracticeCreate(PracticeBase):
    pass


class Practice(PracticeBase):
    id: int
    created_at: datetime.date
    addresses: List[Address] = []
    # employees: List[Employee] = []
    # main_partners: List[Any] = []
    access_systems: List[AccessSystem] = []

    class Config:
        orm_mode = True


class EmployeeBase(BaseModel):
    name: str
    email: str
    professional_num: str
    desktop_num: str = None
    it_portal_num: str = None
    active: bool = True


class EmployeeCreate(EmployeeBase):
    job_title_id: int


class Employee(EmployeeBase):
    id: int
    job_title: JobTitle
    practices: List[Practice] = ""

    class Config:
        orm_mode = True


class RowCount(BaseModel):
    count: int

    class Config:
        orm_mode = True


class EntityNames(BaseModel):
    names: List[str]

    class Config:
        orm_mode = True


class EmployeesForPractice(BaseModel):
    practice_id: int
    employees: List[Employee] = []

    class Config:
        orm_mode = True


class StagingPracticeCreateRequest(PracticeCreate):
    source_id: int = None
    requestor_id: int

    class Config:
        orm_mode = True


class StagingPracticeRequest(PracticeCreate):
    id: int
    last_modified: datetime.datetime
    source_id: int = None
    source: Practice = None
    requestor: Employee
    approver: Employee = None
    approved: bool = None

    class Config:
        orm_mode = True


class StagingEmployeeCreateRequest(EmployeeCreate):
    source_id: int = None
    requestor_id: int
    practice_name: str

    class Config:
        orm_mode = True


class StagingEmployeeRequest(EmployeeCreate):
    id: int
    last_modified: datetime.datetime = None
    source_id: int = None
    source: Employee = None
    requestor: Employee
    approver: Employee = None
    practice_name: str = None
    approved: bool = None
    job_title_id: int

    class Config:
        orm_mode = True


class StagingChangeRequest(BaseModel):
    """
    target_id is optional because if it's adding a new thing, there will be
    no target_id in the table. This is signalled by the modify flag
    """
    requestor_id: int
    target_table: str
    target_id: int = None
    link: bool
    payload: Union[AddressCreate, EmployeeCreate, IPRangeCreate, PracticeCreate, Association]
    # payload: dict

    class Config:
        orm_mode = True


class StagingChangeResponse(BaseModel):
    """
    Response model for any staging change
    """
    id: int
    last_modified: datetime.datetime
    requestor: Employee
    approver: Employee = None
    approved: bool = None
    target_table: str
    target_id: int = None
    link: bool
    payload: dict

    class Config:
        orm_mode = True


class StagingChangeDeltaResponse(BaseModel):
    deltas: dict

    class Config:
        orm_mode = False