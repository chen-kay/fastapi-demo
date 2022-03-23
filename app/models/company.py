"""Company Model."""
from app.db.base_class import Base
from sqlalchemy import Column, Date, Integer, String


class Company(Base):
    """企业"""

    code = Column(String, comment="唯一编码", index=True, unique=True)
    name = Column(String, comment="企业名称")

    shortName = Column(String, comment="简称")
    website = Column(String, comment="官网")

    sort = Column(Integer, comment="顺序", default=100, server_default="100")
    remark = Column(String, comment="备注")

    status = Column(
        Integer,
        comment="状态 1.启用 2.禁用 3.到期",
        default=1,
        server_default="1",
    )
    expireAt = Column(Date, comment="到期时间")

    __table__args__ = {
        "comment": "企业",
    }
