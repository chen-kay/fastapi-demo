"""Schemas Enterp Model."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class EnterpFilter(BaseModel):
    page: int
    page_size: int
    keyword: Optional[str] = ""


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


class EnterpUpdate(BaseModel):
    name: str
    short_name: str = ""
    website: str = ""
    desc: str = ""
