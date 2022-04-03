"""DictType Model."""
from app.db.session import Base
from sqlalchemy import Column, Integer, String, Text


class DictType(Base):
    """字典"""

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    code = Column(String(50), comment="唯一编码", index=True)
    name = Column(String(50), comment="字典名")

    sort = Column(Integer, comment="顺序", default=100, server_default="100")
    remark = Column(Text, comment="备注")

    status = Column(Integer, comment="状态 1.正常 2.禁用", default=1, server_default="1")

    __tablename__ = "dict_type"
    __table__args__ = {
        "comment": "字典",
    }
