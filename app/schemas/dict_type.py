"""Schemas DictType Model."""
from pydantic import BaseModel


class DictTypeType(BaseModel):
    id: int

    code: str
    name: str

    sort: int
    remark: str

    class Config:
        orm_mode = True


class DictValueType(BaseModel):
    company_id: int

    code: str
    value: str

    sort: int = 100
    remark: str = ""

    class Config:
        orm_mode = True
