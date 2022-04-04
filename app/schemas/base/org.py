"""Schemas Org Model."""

from pydantic import BaseModel, Field


class OrgModel(BaseModel):
    id: int = Field(..., title="主键")

    parent_id: int = Field(None, title="上级组织")

    code: str = Field(..., title="唯一编码")
    name: str = Field(..., title="组织名称")

    class Config:
        orm_mode = True
