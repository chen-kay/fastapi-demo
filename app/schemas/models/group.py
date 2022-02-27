"""Schemas Group Model."""

from typing import Optional

from pydantic import BaseModel, Field


class GroupFilter(BaseModel):
    page: int
    page_size: int
    keyword: Optional[str] = ""


class GroupModel(BaseModel):
    id: int

    name: str = ""
    desc: str = ""

    visible: int

    class Config:
        orm_mode = True


class GroupCreate(BaseModel):
    pid_id: Optional[int] = None

    name: str = ""
    desc: str = ""

    visible: int


class GroupUpdate(BaseModel):
    name: str = ""
    desc: str = ""

    visible: int


class GroupView(BaseModel):
    id: int

    name: str = Field(..., title="用户组名")

    class Config:
        orm_mode = True
