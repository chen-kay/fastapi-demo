"""Access Services module."""


from app import crud

from .base import BaseService


class EnterpService(BaseService):
    def initializer(self):
        self.access = crud.Access(self.session, self.redis)
