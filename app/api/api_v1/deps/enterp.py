from dataclasses import dataclass
from datetime import date, datetime
from typing import List, Optional

from app.api.deps import PageFilter, PageModel
from app.schemas.models.user import UserView
from fastapi import Query
from pydantic import BaseModel, Field
from pydantic.main import BaseModel


@dataclass
class ApiEnterpFilter(PageFilter):
    expire_at: Optional[List[date]] = Query(None, title="到期时间")
    domain: str = Query("", title="企业域名")
    name: str = Query("", title="企业名称")
    short_name: str = Query("", title="企业简称")
    is_active: Optional[int] = Query(None, title="状态")
    page: int = Query(1, title="页码")
    page_size: int = Query(100, title="分页")
    keyword: Optional[str] = Query("", title="关键字")


class ApiEnterpType(BaseModel):
    id: int
    domain: str = Field(..., title="企业域名")
    name: str = Field(..., title="企业名称")
    short_name: str = Field(None, title="企业简称")

    website: str = Field(None, title="官网")
    desc: str = Field(None, title="备注信息")

    expire_at: date = Field(None, title="企业过期时间")
    is_active: int = Field(None, title="状态")

    alt_user: UserView = Field(None, title="操作人")

    alt_at: datetime = Field(None, title="操作时间")
    add_at: datetime = Field(None, title="创建时间")

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S"),
        }


class ApiEnterpList(PageModel[ApiEnterpType]):
    pass


class ApiEnterpCreate(BaseModel):
    domain: str = Field(..., title="企业域名")
    name: str = Field(..., title="企业名称")
    short_name: str = Field("", title="企业简称")

    website: str = Field("", title="官网")
    desc: str = Field("", title="备注")

    expire_at: date = Field(None, title="过期时间")


class ApiEnterpUpdate(BaseModel):
    name: str = Field(..., title="企业名称")
    short_name: str = Field("", title="企业简称")
    website: str = Field("", title="官网")
    desc: str = Field("", title="备注")

    expire_at: date = Field(None, title="过期时间")


class ApiEnterpStatus(BaseModel):
    is_active: int = Field(None, title="状态")
