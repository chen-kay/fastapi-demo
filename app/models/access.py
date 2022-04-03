"""Access Model."""
from app.db.session import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Access(Base):
    """权限"""

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    title = Column(String(50), comment="模块/权限名称")
    key = Column(String(50), comment="唯一编码", index=True)

    flag = Column(String(10), comment="类型 module:模块 button:操作", index=True)

    parent_id = Column(Integer, ForeignKey("access.id"), comment="上级id", index=True)
    parent = relationship("Access", foreign_keys=[parent_id])

    sort = Column(Integer, comment="顺序", default=100, server_default="100")

    status = Column(Integer, comment="状态 1.正常 2.禁用", default=1, server_default="1")

    __tablename__ = "access"
    __table__args__ = {
        "comment": "权限",
    }
