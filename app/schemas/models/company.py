from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


class CompanyModel(BaseModel):
    id: int = Field(..., title="主键")

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
