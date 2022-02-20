from datetime import datetime

from app.schemas.models.user import UserView
from pydantic import BaseModel, Field


class ApiEnterpType(BaseModel):
    id: int
    domain: str = Field(..., title="企业域名")
    name: str = Field(..., title="企业名称")
    short_name: str = Field(None, title="企业简称")

    uri: str = Field(None, title="官网")

    desc: str = Field(None, title="备注信息")
    encrypt: int = Field(1, title="数据加密 1.加密 0. 不加密")

    expire_at: datetime = Field(None, title="企业过期时间")

    alt_user: UserView = Field(..., title="操作人")
    alt_at: datetime = Field(..., title="操作时间")

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S"),
        }


class ApiEnterpCreate(BaseModel):
    domain: str = Field(..., title="企业域名")
    name: str = Field(..., title="企业名称")
    short_name: str = Field(None, title="企业简称")

    website: str = Field(None, title="官网")
    desc: str = Field(None, title="备注")

    expire_at: datetime = Field(None, title="过期时间")
