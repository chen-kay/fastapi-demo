"""Dept Model."""

from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .relationship import UsersGroups


class Dept(Base):
    """部门"""

    enterp_id = Column(Integer, ForeignKey("enterp.id"))
    enterp = relationship("Enterp", foreign_keys=[enterp_id])
    pid_id = Column(Integer, ForeignKey("group.id"))
    pid = relationship(
        "Group",
        foreign_keys=[pid_id],
        # remote_side=[id],
        # back_populates='children',
        lazy="dynamic",
    )
    # children = relationship('Group', remote_side=[pid_id])

    name = Column(String, comment="用户组名")
    desc = Column(String, comment="备注")

    path = Column(String, comment="路径")

    visible = Column(Integer, comment="可见范围 1.个人 2.仅分组 3.含下级分组")

    add_user_id = Column(Integer, ForeignKey("user.id"))
    add_user = relationship("User", foreign_keys=[add_user_id])
    alt_user_id = Column(Integer, ForeignKey("user.id"))
    alt_user = relationship("User", foreign_keys=[alt_user_id])
    del_user_id = Column(Integer, index=True)

    users = relationship(
        "User", secondary=UsersGroups, back_populates="groups", lazy="dynamic"
    )

    __table_args__ = {
        "comment": "用户组表",
    }
