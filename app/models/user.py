"""User Model."""

from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .relationship import UsersGroups


class User(Base):
    """用户"""

    enterp_id = Column(Integer, ForeignKey("enterp.id"), index=True)
    enterp = relationship("Enterp", foreign_keys=[enterp_id])

    user_name = Column(String, unique=True, index=True, comment="唯一标识")

    username = Column(String, index=True, comment="账号")
    fullname = Column(String, comment="用户名")

    hashed_password = Column(String, nullable=False, comment="密码")

    is_active = Column(Integer, default=1, server_default="1", comment="状态 1.正常 2.禁用")
    is_admin = Column(Integer, default=0, server_default="0", comment="管理员 1.是 0.否")
    is_superuser = Column(
        Integer,
        default=0,
        server_default="0",
        comment="系统管理员 1.是 0.否",
    )

    add_user_id = Column(Integer, ForeignKey("user.id"))
    add_user = relationship("User", foreign_keys=[add_user_id])
    alt_user_id = Column(Integer, ForeignKey("user.id"))
    alt_user = relationship("User", foreign_keys=[alt_user_id])
    del_user_id = Column(Integer, index=True)

    groups = relationship(
        "Group",
        secondary=UsersGroups,
        back_populates="users",
        lazy="dynamic",
    )

    __table_args__ = {
        "comment": "用户表",
    }
