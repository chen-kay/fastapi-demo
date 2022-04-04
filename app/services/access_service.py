from typing import List

from app import schemas
from app.models import Access
from sqlalchemy.orm import Query, Session
from sqlalchemy.sql import or_

from .base import BaseService


class AccessService(BaseService["Access"]):
    async def get_list(
        self,
        db: Session,
        *,
        title: str = None,
        keyword: str = None,
        ids: List[int] = None,
    ):
        qs = self.get_queryset(db)
        if ids:
            qs = qs.filter(Access.id.in_(ids))
        if title:
            qs = qs.filter(Access.title.like(title))
        if keyword:
            qs = qs.filter(
                or_(
                    Access.title.like(f"%{keyword}%"),
                    Access.key.like(f"%{keyword}%"),
                )
            )
        return qs

    def get_pagination(self, data: Query, *, page: int, limit: int):
        return self.pagination(data, page=page, limit=limit)


access = AccessService(Access)
