from dataclasses import dataclass
from typing import Optional

from fastapi import Query


@dataclass
class Pagination:
    page: int = Query(1, title="页码")
    page_size: int = Query(100, title="分页")
    keyword: Optional[str] = Query(None, title="关键字")
