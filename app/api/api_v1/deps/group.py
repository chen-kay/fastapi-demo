from datetime import datetime
from typing import List, Optional

from app.schemas.models.user import UserView
from pydantic import BaseModel, Field


class ApiGroupType(BaseModel):
    id: int

    name: str = Field(..., title="用户组名")
    desc: str = Field(None, title="备注")

    visible: int = Field(..., title="可见范围")

    children: List["ApiGroupType"] = Field(None, title="下级用户组")

    alt_user: UserView = Field(None, title="操作人")
    alt_at: datetime = Field(None, title="操作时间")

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S"),
        }


class ApiGroupList(BaseModel):
    data: List[ApiGroupType] = Field(..., title="用户组数据")


class ApiGroupCreate(BaseModel):
    pid_id: Optional[int] = Field(None, title="上级用户组")

    name: str = Field(..., title="用户组名")
    desc: str = Field(None, title="备注")

    visible: int = Field(1, title="可见范围")


class ApiGroupUpdate(BaseModel):
    name: str = Field(..., title="用户组名")
    desc: str = Field(None, title="备注")

    visible: int = Field(None, title="可见范围")
