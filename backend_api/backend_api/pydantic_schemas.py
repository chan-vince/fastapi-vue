import datetime
from typing import List, Any

from pydantic import BaseModel


class GPAddressBase(BaseModel):
    id: int
    line_1: str
    line_2: str
    town: str
    country: str
    postcode: str
    dts_email: str
    gp_practice_id: int
    gp_practice: Any


class GPAddressCreate(GPAddressBase):
    pass


class GPAddress(GPAddressBase):
    class Config:
        orm_mode = True


class SystemTypeBase(BaseModel):
    id: int
    name: str


class SystemTypeCreate(SystemTypeBase):
    pass


class SystemType(SystemTypeBase):
    class Config:
        orm_mode = True


class JobTitleBase(BaseModel):
    id: int
    title: str


class JobTitleCreate(JobTitleBase):
    pass


class JobTitle(JobTitleBase):
    class Config:
        orm_mode = True


class IPRangesBase(BaseModel):
    id: int
    cidr: str


class IPRangesCreate(IPRangesBase):
    pass


class IPRanges(IPRangesBase):
    class Config:
        orm_mode = True


class GPEmployeeBase(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    professional_num: str
    desktop_num: str
    it_portal_num: str
    active: bool
    job_title_id: int
    job_title: JobTitle
    practices: List[Any] = []


class GPEmployeeCreate(GPEmployeeBase):
    pass


class GPEmployee(GPEmployeeBase):
    class Config:
        orm_mode = True


class GPPracticeBase(BaseModel):
    id: int
    name_ice: str
    created_date: datetime.datetime
    phone_num: str
    emis_cdb_practice_code: str
    go_live_date: datetime.datetime = None
    closed: bool
    main_partner_id: int = None

    address: GPAddress = None
    employees: List[GPEmployee] = []
    main_partner: List[GPEmployee] = []
    system_type: List[SystemType] = []


class GPPracticeCreate(GPPracticeBase):
    pass


class GPPractice(GPPracticeBase):
    class Config:
        orm_mode = True


GPPractice.update_forward_refs()