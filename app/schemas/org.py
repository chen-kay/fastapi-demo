"""Schemas Org Model."""
from dataclasses import dataclass
from typing import List, Optional

from fastapi import Query
from pydantic import BaseModel, Field

from .base import Pagination


@dataclass
class OrgQuery(Pagination):
    name: str = Query(None, title="机构名称")
    parent_id: int = Query(None, title="上级机构")


class OrgType(BaseModel):
    id: int = Field(..., title="主键")

    parent_id: int = Field(None, title="上级组织")
    parent_ids: List[int] = Field([], title="上级组织")

    code: str = Field(..., title="唯一编码")
    name: str = Field(..., title="组织名称")

    sort: int = Field(100, title="顺序")
    remark: str = Field("", title="备注")

    class Config:
        orm_mode = True


class OrgAdd(BaseModel):
    parent_id: int = Field(0, title="上级组织")

    code: str = Field(..., title="唯一编码")
    name: str = Field(..., title="组织名称")

    sort: int = Field(100, title="顺序")
    remark: str = Field("", title="备注")

    class Config:
        orm_mode = True


class OrgEdit(BaseModel):
    parent_id: int = Field(0, title="上级组织")

    code: str = Field(..., title="唯一编码")
    name: str = Field(..., title="组织名称")

    sort: int = Field(100, title="顺序")
    remark: str = Field("", title="备注")

    class Config:
        orm_mode = True


class OrgTree(BaseModel):
    key: int = Field(..., title="主键", alias="主键")
    value: str = Field(..., title="主键", alias="id")
    title: str = Field(..., title="组织名称", alias="name")
    label: str = Field(..., title="组织名称", alias="name")

    parent_id: int = Field(..., title="上级组织")
    children: List["OrgTree"] = []

    class Config:
        orm_mode = True
