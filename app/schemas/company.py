"""Schemas Company Model."""
from dataclasses import dataclass
from datetime import date
from typing import List, Literal, Optional

from fastapi import Query
from pydantic import BaseModel, Field

from .base import Pagination


@dataclass
class CompanyFilter(Pagination):
    expire_at: Optional[List[date]] = Query(None, title="到期时间")
    status: Optional[Literal["1", "2", "3"]] = Query(None, title="状态 1.启用 2.禁用 3.到期")


class CompanyType(BaseModel):
    id: int = Field(..., title="主键")

    domain: str = Field(..., title="域名")
    name: str = Field(..., title="企业名称")

    short_name: str = Field(None, title="简称")
    website: str = Field(None, title="官网")

    sort: int = Field(None, title="顺序")
    remark: str = Field(None, title="备注")

    status: int = Field(..., title="状态 1.启用 2.禁用 3.到期")
    expire_at: date = Field(None, title="到期时间")

    class Config:
        orm_mode = True


class CompanyAdd(BaseModel):
    domain: str = Field(..., title="域名")
    name: str = Field(..., title="企业名称")

    short_name: str = Field(None, title="简称")
    website: str = Field(None, title="官网")

    sort: int = Field(None, title="顺序")
    remark: str = Field(None, title="备注")

    status: Literal[1, 2] = Field(..., title="状态 1.启用 2.禁用 3.到期")
    expire_at: date = Field(None, title="到期时间")

    class Config:
        orm_mode = True


class CompanyEdit(BaseModel):
    name: str = Field(..., title="企业名称")

    short_name: str = Field(None, title="简称")
    website: str = Field(None, title="官网")

    sort: int = Field(None, title="顺序")
    remark: str = Field(None, title="备注")

    status: Literal[1, 2] = Field(..., title="状态 1.启用 2.禁用 3.到期")
    expire_at: date = Field(None, title="到期时间")

    class Config:
        orm_mode = True


class CompanyOption(BaseModel):
    key: int = Field(..., title="key", alias="id")
    value: int = Field(..., title="值", alias="id")
    label: str = Field(..., title="标签", alias="short_name")
    title: str = Field(..., title="标题", alias="name")

    class Config:
        orm_mode = True
