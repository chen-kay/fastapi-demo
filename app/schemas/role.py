"""Schemas Role Model."""
from dataclasses import dataclass
from typing import List, Optional

from fastapi import Query
from pydantic import BaseModel, Field

from .base import Pagination


@dataclass
class RoleQuery(Pagination):
    name: str = Query(None, title="角色名称")
    company_id: int = Query(None, title="归属企业")


class RoleType(BaseModel):
    id: int = Field(..., title="主键")

    code: str = Field(..., title="唯一编码")
    name: str = Field(..., title="角色名称")

    sort: int = Field(100, title="顺序")
    remark: str = Field("", title="备注")

    class Config:
        orm_mode = True


class RoleAdd(BaseModel):
    company_id: Optional[int] = Field(None, title="归属企业")

    code: str = Field(..., title="唯一编码")
    name: str = Field(..., title="角色名称")

    sort: int = Field(100, title="顺序")
    remark: str = Field("", title="备注")

    class Config:
        orm_mode = True


class RoleEdit(BaseModel):
    code: str = Field(..., title="唯一编码")
    name: str = Field(..., title="角色名称")

    sort: int = Field(100, title="顺序")
    remark: str = Field("", title="备注")

    class Config:
        orm_mode = True


class RoleOption(BaseModel):
    key: int = Field(..., title="主键", alias="主键")
    value: str = Field(..., title="主键", alias="id")
    title: str = Field(..., title="角色名称", alias="name")
    label: str = Field(..., title="角色名称", alias="name")

    class Config:
        orm_mode = True


class RoleGrantMenu(BaseModel):
    access_ids: List[int] = Field(None, title="授权权限id")


class RoleGrantData(BaseModel):
    dataScopeType: int = Field(..., title="授权范围")
    org_ids: List[int] = Field(None, title="授权组织id")


class RoleOwnMenu(BaseModel):
    access_ids: List[int] = Field(None, title="授权权限id")

    class Config:
        orm_mode = True


class RoleOwnData(BaseModel):
    dataScopeType: int = Field(..., title="授权范围")
    org_ids: List[int] = Field(None, title="授权组织id")

    class Config:
        orm_mode = True
