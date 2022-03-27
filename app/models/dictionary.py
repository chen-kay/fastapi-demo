"""Dictionary Model."""
from app.db.base_class import Base
from sqlalchemy import Column, Integer, String


class Dictionary(Base):
    """字典"""

    code = Column(String, comment="唯一编码", index=True)
    name = Column(String, comment="字典名")

    sort = Column(Integer, comment="顺序", default=100, server_default="100")
    remark = Column(String, comment="备注")

    status = Column(Integer, comment="状态 1.正常 2.禁用", default=1, server_default="1")

    __table__args__ = {
        "comment": "字典",
    }


class DictValue(Base):
    """字典值"""

    company_id = Column(Integer, comment="企业id", index=True)
    parent_id = Column(Integer, comment="字典id", index=True)

    code = Column(String, comment="唯一编码", index=True)
    value = Column(String, comment="值")

    sort = Column(Integer, comment="顺序", default=100, server_default="100")
    remark = Column(String, comment="备注")

    __table__args__ = {
        "comment": "字典值",
    }
