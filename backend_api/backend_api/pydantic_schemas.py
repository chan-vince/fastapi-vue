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
    gp_practice_id: int
    gp_practice: Any

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


class GPEmployeeBase(BaseModel):
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
    id: int

    class Config:
        orm_mode = True


class GPPracticeBase(BaseModel):
    name: str
    phone_num: str
    emis_cdb_practice_code: str
    go_live_date: datetime.datetime = None
    closed: bool


class GPPracticeCreate(GPPracticeBase):
    pass


class GPPractice(GPPracticeBase):
    id: int

    created_date: datetime.datetime
    address: GPAddress = None
    employees: List[GPEmployee] = []
    main_partners: List[GPEmployee] = []
    system_type: List[SystemType] = []

    class Config:
        orm_mode = True
