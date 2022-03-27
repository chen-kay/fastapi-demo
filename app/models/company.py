"""Company Model."""

from app.db.base_class import Base
from sqlalchemy import Column, Date, Integer, String


class Company(Base):
    """企业"""

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    code = Column(String, comment="唯一编码", index=True, unique=True)
    name = Column(String, comment="企业名称")

    short_name = Column(String, comment="简称")
    website = Column(String, comment="官网")

    sort = Column(Integer, comment="顺序", default=100, server_default="100")
    remark = Column(String, comment="备注")

    status = Column(
        Integer,
        comment="状态 1.启用 2.禁用 3.到期",
        default=1,
        server_default="1",
    )
    expire_at = Column(Date, comment="到期时间")

    is_del = Column(
        Integer,
        default=0,
        server_default="0",
        comment="逻辑删除:0=未删除,1=删除",
    )
    __table__args__ = {
        "comment": "企业",
    }
