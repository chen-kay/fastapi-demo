"""Company Model."""

from app.db.session import Base
from sqlalchemy import Column, Date, Integer, String, Text


class Company(Base):
    """企业"""

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    domain = Column(String(50), comment="域名", index=True, unique=True)
    name = Column(String(50), comment="企业名称")

    short_name = Column(String(20), comment="简称")
    website = Column(String(50), comment="官网")

    sort = Column(Integer, comment="顺序", default=100, server_default="100")
    remark = Column(Text, comment="备注")

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

    __tablename__ = "company"
    __table__args__ = {
        "comment": "企业",
    }
