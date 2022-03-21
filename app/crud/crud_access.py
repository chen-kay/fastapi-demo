from app.models import Access

from .base import BaseCrud


class AccessCrud(BaseCrud[Access]):
    model = Access

    async def get_access_list(self, *, is_super: bool = False):
        qs = self.session.query(Access).filter(Access.is_del == 0)
        if not is_super:
            qs = qs.filter(Access.is_super == is_super)
        return qs.all()
