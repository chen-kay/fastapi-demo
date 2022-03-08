"""Schemas Enterp Model."""

from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel


class EnterpFilter(BaseModel):
    domain: Optional[str] = ""
    name: Optional[str] = ""
    short_name: Optional[str] = ""
    expire_at: List[date] = []
    is_active: Optional[int] = None

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

    expire_at: date = None


class EnterpUpdate(BaseModel):
    name: str
    short_name: str = ""
    website: str = ""
    desc: str = ""

    expire_at: date = None
