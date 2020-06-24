import datetime
from typing import List, Any, Union

from pydantic import BaseModel


class GPAddressBase(BaseModel):
    line_1: str
    line_2: Union[str, None]
    town: str
    county: str
    postcode: str
    dts_email: str


class GPAddressCreate(GPAddressBase):
    pass


class GPAddress(GPAddressBase):
    id: int
    practice_id: int

    class Config:
        orm_mode = True


class SystemTypeBase(BaseModel):
    name: str


class SystemTypeCreate(SystemTypeBase):
    pass


class SystemType(SystemTypeBase):
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


class IPRangesBase(BaseModel):
    cidr: str


class IPRangesCreate(IPRangesBase):
    pass


class IPRanges(IPRangesBase):
    id: int

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
    job_title_id: int = None


class EmployeeCreate(EmployeeBase):
    pass


class Employee(EmployeeBase):
    id: int
    practices: List[Any] = []

    class Config:
        orm_mode = True


class PracticeBase(BaseModel):
    name: str
    phone_num: str
    emis_cdb_practice_code: str
    go_live_date: datetime.datetime = None
    closed: bool


class PracticeCreate(PracticeBase):
    pass


class Practice(PracticeBase):
    id: int

    created_date: datetime.datetime
    address: GPAddress = None
    employees: List[Employee] = []
    main_partners: List[Employee] = []
    system_type: List[SystemType] = []

    class Config:
        orm_mode = True
