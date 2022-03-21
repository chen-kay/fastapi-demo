"""RelationShip Model."""

from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, Integer, Table

GroupsAccess = Table(
    "groups_access",
    Base.metadata,
    Column(
        "group_id",
        Integer,
        ForeignKey("group.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "access_id",
        Integer,
        ForeignKey("access.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    ),
)

UsersGroups = Table(
    "users_groups",
    Base.metadata,
    Column(
        "user_id",
        Integer,
        ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "group_id",
        Integer,
        ForeignKey("group.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    ),
)
