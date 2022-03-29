from app.models import User

from .base import BaseCrud


class CrudUser(BaseCrud["User"]):
    model = User
