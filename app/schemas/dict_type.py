"""Schemas DictType Model."""
from typing import Optional

from pydantic import BaseModel, Field


class DictTypeType(BaseModel):
    id: int = Field(..., title="主键")

    code: str = Field(..., title="唯一编码")
    name: str = Field(..., title="字典名")

    sort: Optional[int] = Field(None, title="顺序")
    remark: Optional[str] = Field(None, title="备注")

    status: int = Field(..., title="状态")

    class Config:
        orm_mode = True
