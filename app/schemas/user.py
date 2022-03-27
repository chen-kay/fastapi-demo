"""Schemas User Model."""

from datetime import date
from typing import Optional

from pydantic import BaseModel


class UserModel(BaseModel):
    id: int
    company_id: Optional[int] = None

    username: str
    fullname: str = None

    nickname: str = None

    birth: date = None
    sex: int = None

    email: str = None
    mobile: str = None

    status: int
    is_admin: int
    is_superuser: int

    class Config:
        orm_mode = True
