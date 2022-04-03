"""DictData Model."""
from app.db.session import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship


class DictData(Base):
    """字典数据"""

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    company_id = Column(Integer, ForeignKey("company.id"), comment="企业id", index=True)
    company = relationship("Company", foreign_keys=[company_id])
    parent_id = Column(Integer, ForeignKey("dict_type.id"), comment="字典id", index=True)
    parent = relationship("DictType", foreign_keys=[parent_id])

    code = Column(String(50), comment="唯一编码", index=True)
    value = Column(String(50), comment="值")

    sort = Column(Integer, comment="顺序", default=100, server_default="100")
    remark = Column(Text, comment="备注")

    is_del = Column(
        Integer,
        default=0,
        server_default="0",
        comment="逻辑删除:0=未删除,1=删除",
    )

    __tablename__ = "dict_data"
    __table__args__ = {
        "comment": "字典数据",
    }
