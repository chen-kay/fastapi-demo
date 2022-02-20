"""Menu Model."""

from app.db.base_class import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .relationship import GroupsAuthoritys


class Authority(Base):
    """权限"""

    pid_id = Column(Integer, index=True)

    flag = Column(String, comment="类型 menu:模块 button:按钮")

    title = Column(String, nullable=False, comment="模块/权限名称")
    key = Column(String, index=True, unique=True, comment="模块/权限key")

    sort = Column(Integer, default=1, server_default="1", comment="排序")

    is_active = Column(Integer, default=1, server_default="1", comment="状态 1.正常 2.禁用")

    groups = relationship(
        "Group", secondary=GroupsAuthoritys, back_populates="authoritys", lazy="dynamic"
    )

    __table_args__ = {
        "comment": "菜单权限表",
    }
