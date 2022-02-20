"""Schemas Enterp Model."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class EnterpModel(BaseModel):
    id: int
    domain: str

    name: str = ""
    short_name: str = ""
    website: str = ""
    desc: str = ""

    is_active: int
    expire_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class EnterpCreate(BaseModel):
    domain: str
