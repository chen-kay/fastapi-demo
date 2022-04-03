from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, Field


class UserModel(BaseModel):
    id: int = Field(..., title='主键')
    company_id: Optional[int] = Field(None, title="归属企业")
    org_id: int = Field(0, title="归属组织")

    username: str = Field(..., title="账号", max_length=50)
    fullname: str = Field(..., title="姓名", max_length=50)

    nickname: str = Field(None, title="昵称", max_length=50)

    password: str = Field("123456", title="密码")

    birth: date = Field(None, title="生日")
    sex: int = Field(None, title="性别 0.无 1.男 2.女")

    email: str = Field(None, title="邮箱", max_length=50)
    mobile: str = Field(None, title="手机号", max_length=50)

    status: Literal[1, 2] = Field(1, title="状态")
    is_admin: int = Field(0, title="是否管理员")
    is_superuser: int = Field(0, title="是否超级管理员")

    class Config:
        orm_mode = True
