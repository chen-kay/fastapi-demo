"""Access Model."""
from app.db.base_class import Base
from sqlalchemy import Column, Integer, String


class Access(Base):
    """权限"""

    title = Column(String, comment="模块/权限名称")
    key = Column(String, comment="唯一编码", index=True)

    flag = Column(String, comment="类型 module:模块 button:操作", index=True)

    parent_id = Column(Integer, comment="上级id", index=True)

    sort = Column(Integer, comment="顺序", default=100, server_default="100")

    status = Column(Integer, comment="状态 1.正常 2.禁用", default=1, server_default="1")

    __table__args__ = {
        "comment": "权限",
    }
