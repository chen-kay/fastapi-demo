from dataclasses import dataclass
from datetime import datetime
from typing import Generic, List, Optional, TypeVar

from fastapi import Query
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar("T", bound=BaseModel)


@dataclass
class PageFilter:
    page: int = Query(1, title="页码")
    page_size: int = Query(100, title="分页")
    keyword: Optional[str] = Query("", title="关键字")


class Pageination(GenericModel, Generic[T]):
    total: int = Field(..., title="总数")
    data: List[T] = Field(..., titlt="分页数据")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S"),
        }
