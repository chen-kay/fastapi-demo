"""Schemas DictData Model."""
from dataclasses import dataclass
from typing import Optional

from fastapi import Query
from pydantic import BaseModel, Field

from .base import Pagination


@dataclass
class DictDataFilter(Pagination):
    parent_id: Optional[int] = Query(None, title="归属字典id")


class DictDataType(BaseModel):
    id: int = Field(..., title="主键")

    code: str = Field(..., title="唯一编码")
    value: str = Field(..., title="字典值")

    sort: Optional[int] = Field(None, title="顺序")
    remark: Optional[str] = Field(None, title="备注")

    class Config:
        orm_mode = True


class DictDataAdd(BaseModel):
    parent_id: int = Field(..., title="归属字典id")

    code: str = Field(..., title="唯一编码")
    value: str = Field(..., title="字典值")

    sort: Optional[int] = Field(None, title="顺序")
    remark: Optional[str] = Field(None, title="备注")

    class Config:
        orm_mode = True


class DictDataEdit(BaseModel):
    code: str = Field(..., title="唯一编码")
    value: str = Field(..., title="字典值")

    sort: Optional[int] = Field(None, title="顺序")
    remark: Optional[str] = Field(None, title="备注")

    class Config:
        orm_mode = True
