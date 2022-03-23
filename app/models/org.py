"""Org Model."""
from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Org(Base):
    """组织"""

    company_id = Column(Integer, ForeignKey("company.id"))
    company = relationship("Company", foreign_keys=[company_id])
    parent_id = Column(Integer, ForeignKey("parent.id"))
    parent = relationship("Org", foreign_keys=[parent_id])

    code = Column(String, comment="唯一编码", index=True)
    name = Column(String, comment="组织名称")

    sort = Column(Integer, comment="顺序", default=100, server_default="100")
    remark = Column(String, comment="备注")

    status = Column(Integer, comment="状态 1.正常 2.禁用", default=1, server_default="1")

    __table__args__ = {
        "comment": "组织",
    }
