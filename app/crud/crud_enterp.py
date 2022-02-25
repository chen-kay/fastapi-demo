from app.models import Enterp
from sqlalchemy.orm import Session
from sqlalchemy.sql import or_

from .base import BaseCrud


class EnterpCrud(BaseCrud[Enterp]):
    model = Enterp

    async def get_enterp_list(
        self,
        session: Session,
        *,
        keyword: str,
        is_active: int = None,
        page: int,
        page_size: int,
    ):
        qs = session.query(Enterp).filter(Enterp.is_del == 0)
        if is_active:
            qs = qs.filter(Enterp.is_active == is_active)
        if keyword:
            qs = qs.filter(
                or_(
                    Enterp.domain.like(f"%{keyword}%"),
                    Enterp.name.like(f"%{keyword}%"),
                    Enterp.short_name.like(f"%{keyword}%"),
                )
            )

        total = qs.count()
        qs = qs.offset((page - 1) * page_size).limit(page_size).all()
        return qs, total

    async def get_by_domain(self, session: Session, *, domain: str):
        ins = (
            session.query(Enterp)
            .filter(Enterp.domain == domain, Enterp.is_del == 0)
            .first()
        )
        return ins


enterp = EnterpCrud(Enterp)
