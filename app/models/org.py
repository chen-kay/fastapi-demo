"""Org Model."""
from app.db.session import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship


class Org(Base):
    """组织"""

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    company_id = Column(Integer, ForeignKey("company.id"), comment="企业id", index=True)
    company = relationship("Company", backref="orgs", remote_side="Company.id")
    parent_id = Column(Integer, ForeignKey("org.id"), comment="上级组织", index=True)
    parent = relationship("Org", backref="orgs", remote_side="Org.id")

    code = Column(String(50), comment="唯一编码", index=True)
    name = Column(String(50), comment="组织名称")

    sort = Column(Integer, comment="顺序", default=100, server_default="100")
    remark = Column(Text, comment="备注")

    status = Column(Integer, comment="状态 1.正常 2.禁用", default=1, server_default="1")

    is_del = Column(
        Integer,
        default=0,
        server_default="0",
        comment="逻辑删除:0=未删除,1=删除",
    )

    __tablename__ = "org"
    __table__args__ = {
        "comment": "组织",
    }
