from app.models import User

from .base import BaseCrud


class CrudUser(BaseCrud):
    model = User

    async def get_by_username(self, username: str):
        qs = self.session.query(User).filter(
            User.is_del == 0,
            User.username == username,
        )
        ins = qs.first()
        return ins
