"""Schemas User Model."""

from typing import Optional

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

