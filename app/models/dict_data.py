"""DictData Model."""
from app.db.base_class import Base
from sqlalchemy import Column, Integer, String


class DictData(Base):
    """字典数据"""

    company_id = Column(Integer, comment="企业id", index=True)
    parent_id = Column(Integer, comment="字典id", index=True)

    code = Column(String, comment="唯一编码", index=True)
    value = Column(String, comment="值")

    sort = Column(Integer, comment="顺序", default=100, server_default="100")
    remark = Column(String, comment="备注")

    __table__args__ = {
        "comment": "字典数据",
    }
