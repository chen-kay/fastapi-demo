"""Schemas User Model."""

from typing import List, Optional

from pydantic import BaseModel


class UserModel(BaseModel):
    id: int
    enterp_id: Optional[int] = None
    user_name: str

    username: str
    fullname: str

    is_active: int
    is_admin: int
    is_superuser: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    enterp_id: Optional[int] = None

    user_name: str
    username: str
    fullname: str

    password: str = "123456"

    is_active: int = 1
    is_admin: int = 0

    add_user_id: Optional[int] = None
    alt_user_id: Optional[int] = None

    groups: List[int] = []
