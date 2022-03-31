"""Schemas Company Model."""
from datetime import date

from pydantic import BaseModel


class CompanyModel(BaseModel):
    id: int

    domain: str = ""
    name: str = ""

    short_name: str = ""
    website: str = ""

    sort: int = 100
    remark: str = ""

    status: int
    expire_at: date = None

    class Config:
        orm_mode = True


class CompanyType(BaseModel):
    id: int

    domain: str
    name: str

    short_name: str = ""
    website: str = ""

    sort: int
    remark: str

    status: int
    expire_at: date = None

    class Config:
        orm_mode = True


class CompanyAdd(BaseModel):
    domain: str
    name: str

    short_name: str = ""
    website: str = ""

    sort: int
    remark: str

    status: int
    expire_at: date = None

    class Config:
        orm_mode = True


class CompanyEdit(BaseModel):
    name: str

    short_name: str = ""
    website: str = ""

    sort: int
    remark: str

    class Config:
        orm_mode = True
