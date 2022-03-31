"""DictData Model."""
from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class DictData(Base):
    """字典数据"""

    company_id = Column(Integer, ForeignKey("company.id"), comment="企业id", index=True)
    company = relationship("Company", foreign_keys=[company_id])
    parent_id = Column(Integer, ForeignKey("dict_type.id"), comment="字典id", index=True)
    parent = relationship("DictType", foreign_keys=[parent_id])

    code = Column(String, comment="唯一编码", index=True)
    value = Column(String, comment="值")

    sort = Column(Integer, comment="顺序", default=100, server_default="100")
    remark = Column(String, comment="备注")

    __table__args__ = {
        "comment": "字典数据",
    }
