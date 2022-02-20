"""Schemas Enterp Model."""

from datetime import datetime

from pydantic import BaseModel


class EnterpModel(BaseModel):
    id: int
    domain: str

    name: str = ""
    short_name: str = ""
    website: str = ""
    desc: str = ""

    is_active: int
    expire_at: datetime = None

    class Config:
        orm_mode = True


class EnterpCreate(BaseModel):
    domain: str
    name: str
    short_name: str = ""

    website: str = ""
    desc: str = ""

    expire_at: datetime = None

    add_user_id: int
    alt_user_id: int
