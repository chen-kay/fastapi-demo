from datetime import datetime
from typing import List, Optional

from app.schemas.models.user import UserView
from pydantic import BaseModel, Field


class ApiEnterpFilter(BaseModel):
    page: int = Field(1, title="页码")
    page_size: int = Field(100, title="分页")
    keyword: Optional[str] = Field("", title="关键字")


class ApiEnterpType(BaseModel):
    id: int
    domain: str = Field(..., title="企业域名")
    name: str = Field(..., title="企业名称")
    short_name: str = Field(None, title="企业简称")

    website: str = Field(None, title="官网")
    desc: str = Field(None, title="备注信息")

    expire_at: datetime = Field(None, title="企业过期时间")

    alt_user: UserView = Field(None, title="操作人")
    alt_at: datetime = Field(None, title="操作时间")

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S"),
        }


class ApiEnterpList(BaseModel):
    data: List[ApiEnterpType] = Field(..., title="企业数据")
    total: int = Field(..., title="总条数")

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S"),
        }


class ApiEnterpCreate(BaseModel):
    domain: str = Field(..., title="企业域名")
    name: str = Field(..., title="企业名称")
    short_name: str = Field("", title="企业简称")

    website: str = Field("", title="官网")
    desc: str = Field("", title="备注")

    expire_at: datetime = Field(None, title="过期时间")


class ApiEnterpUpdate(BaseModel):
    name: str = Field(..., title="企业名称")
    short_name: str = Field("", title="企业简称")
    website: str = Field("", title="官网")
    desc: str = Field("", title="备注")

    expire_at: datetime = Field(None, title="过期时间")
