import datetime
from typing import List, Union

from pydantic import BaseModel, validator


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
    practice_id: Union[int, None]
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
    ip_ranges: List[IPRange] = []

    class Config:
        orm_mode = True


class AccessSystemBase(BaseModel):
    name: str


class AccessSystem(AccessSystemBase):
    id: int

    class Config:
        orm_mode = True


class AccessSystemCreate(AccessSystemBase):
    pass


class Link(BaseModel):
    # link: str
    action: str
    data: List[Union[AccessSystem]]

    # @validator('link')
    # def link_must_be_one_of(cls, v):
    #     allowed = ["access_systems", "addresses"]
    #     if v not in allowed:
    #         raise ValueError
    #     return v

    @validator('action')
    def action_must_be_one_of(cls, v):
        allowed = ["add", "remove", "replace"]
        if v not in allowed:
            raise ValueError
        return v

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
    practice_ids: List[int] = None


class Employee(EmployeeBase):
    id: int
    job_title: JobTitle
    practices: List[Practice] = None

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


class ChangeRequest(BaseModel):
    requestor_id: int
    target_name: str
    target_id: int = None
    current_state: Union[Employee, Practice] = {}
    new_state: Union[EmployeeCreate, PracticeCreate, Link]

    @validator('target_name')
    def target_name_must_be_one_of(cls, v):
        names = ["employee", "practice", "ip_range", "address", "practice.access_systems"]
        if v not in names:
            raise ValueError(f"target_name must be one of {', '.join(names)}")
        return v

    class Config:
        orm_mode = True


class ChangeResponse(BaseModel):
    """
    Response model for any staging change
    """
    id: int
    created_at: datetime.datetime
    last_modified: datetime.datetime
    requestor_id: int
    requestor: Employee
    approver: Employee = None
    approver_id: Union[int, None] = 1
    approval_status: bool = None
    target_name: str
    target_id: int = None
    current_state: dict = None
    new_state: dict

    class Config:
        orm_mode = True


class StagingChangeDeltaResponse(BaseModel):
    deltas: dict

    class Config:
        orm_mode = False
