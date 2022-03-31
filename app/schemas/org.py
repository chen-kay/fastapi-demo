"""Schemas Org Model."""
from dataclasses import dataclass
from typing import List, Literal, Optional

from fastapi import Query
from pydantic import BaseModel, Field


class OrgType(BaseModel):
    id: int = Field(..., title="主键")

    code: str = Field(..., title="唯一编码")
    name: str = Field(..., title="组织名称")

    sort: int = Field(100, title="顺序")
    remark: str = Field("", title="备注")

    status: Literal[1, 2] = Field(1, title="状态")

    class Config:
        orm_mode = True


@dataclass
class OrgQuery:
    name: str = Query(None, title="机构名称")
    parent_id: int = Query(None, title="上级机构")

    page: int = Query(1, title="页码")
    page_size: int = Query(100, title="分页")


class OrgAdd(BaseModel):
    company_id: Optional[int] = Field(None, title="归属企业")
    parent_id: int = Field(0, title="上级组织")

    code: str = Field(..., title="唯一编码")
    name: str = Field(..., title="组织名称")

    sort: int = Field(100, title="顺序")
    remark: str = Field("", title="备注")

    status: Literal[1, 2] = Field(1, title="状态")

    class Config:
        orm_mode = True


class OrgEdit(BaseModel):
    parent_id: int = Field(0, title="上级组织")

    code: str = Field(..., title="唯一编码")
    name: str = Field(..., title="组织名称")

    sort: int = Field(100, title="顺序")
    remark: str = Field("", title="备注")

    status: Literal[1, 2] = Field(1, title="状态")

    class Config:
        orm_mode = True


class OrgTree(BaseModel):
    id: int = Field(..., title="主键")
    parent_id: int = Field(..., title="上级组织")
    value: str = Field(..., title="主键", alias="id")
    title: str = Field(..., title="组织名称", alias="name")
    label: str = Field(..., title="组织名称", alias="name")

    children: List["OrgTree"] = []

    class Config:
        orm_mode = True
