import datetime
from typing import List, Any, Union
from pydantic import BaseModel


class AddressBase(BaseModel):
    line_1: str
    line_2: Union[str, None]
    town: str
    county: str
    postcode: str
    dts_email: str


class AddressCreate(AddressBase):
    pass


class Address(AddressBase):
    id: int
    practice_id: Union[int, None]

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


class IPRangeBase(BaseModel):
    cidr: str


class IPRangeCreate(IPRangeBase):
    pass


class IPRange(IPRangeBase):
    id: int
    practice: int

    class Config:
        orm_mode = True


class PracticeBase(BaseModel):
    name: str
    phone_num: str
    national_code: str
    emis_cdb_practice_code: str
    go_live_date: datetime.datetime = None
    closed: bool


class PracticeCreate(PracticeBase):
    pass


class Practice(PracticeBase):
    id: int
    created_date: datetime.datetime
    addresses: List[Address] = []
    # employees: List[Employee] = []
    # main_partners: List[Employee] = []
    access_systems: List[AccessSystem] = []
    ip_ranges: List[IPRange] = []


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
    practices: List[Practice]

    class Config:
        orm_mode = True
