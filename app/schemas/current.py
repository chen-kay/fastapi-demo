from typing import List

from pydantic import BaseModel


class CurrentType(BaseModel):
    id: int

    username: str
    fullname: str = ""

    authoritys: List[str] = []

    user_name: str

    class Config:
        orm_mode = True
