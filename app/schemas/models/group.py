"""Schemas Group Model."""

from typing import Optional

from pydantic import BaseModel, Field


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

    visible: int = 1


class GroupUpdate(BaseModel):
    pid_id: Optional[int] = None

    name: str = ""
    desc: str = ""

    visible: int = 1


class GroupView(BaseModel):
    id: int

    name: str = Field(..., title="用户组名")

    class Config:
        orm_mode = True
