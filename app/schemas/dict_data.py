"""Schemas DictData Model."""
from pydantic import BaseModel


class DictDataType(BaseModel):
    id: int

    code: str
    value: str

    sort: int
    remark: str

    class Config:
        orm_mode = True


class DictDataAdd(BaseModel):
    company_id: int = None
    parent_id: int

    code: str
    value: str

    sort: int = 100
    remark: str = ""

    class Config:
        orm_mode = True


class DictDataEdit(BaseModel):
    code: str
    value: str

    sort: int = 100
    remark: str = ""

    class Config:
        orm_mode = True
