"""RelationShip Model."""

from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, Integer, Table

GroupsAuthoritys = Table(
    "groups_authoritys",
    Base.metadata,
    Column(
        "group_id",
        Integer,
        ForeignKey("group.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "authority_id",
        Integer,
        ForeignKey("authority.id", onupdate="CASCADE", ondelete="CASCADE"),
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
