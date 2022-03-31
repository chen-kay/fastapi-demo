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
