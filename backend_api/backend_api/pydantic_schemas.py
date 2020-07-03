import datetime
from typing import List, Any, Union
from pydantic import BaseModel


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
    go_live_date: datetime.date
    closed: bool


class PracticeCreate(PracticeBase):
    pass


class Practice(PracticeBase):
    id: int
    created_at: datetime.date
    addresses: List[Address] = []
    # employees: List[Employee] = []
    main_partners: List[Any] = []
    access_systems: List[AccessSystem] = []

    class Config:
        orm_mode = True


class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    professional_num: str
    desktop_num: str = None
    it_portal_num: str = None
    active: bool = True


class EmployeeCreate(EmployeeBase):
    job_title_id: int


class Employee(EmployeeBase):
    id: int
    job_title: JobTitle = None

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
    employees: List[Employee]

    class Config:
        orm_mode = True


class StagingPracticeRequest(PracticeCreate):
    source_id: int
    requestor_id: int


class StagingRequest(PracticeCreate):
    id: int
    last_modified: datetime.datetime
    source_id: int
    source: Practice
    requestor: Employee
    approver: Employee = None
    approved: bool = None

    class Config:
        orm_mode = True
