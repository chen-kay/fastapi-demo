"""Enterp Model."""

from app.db.base_class import Base
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship


class Enterp(Base):
    domain = Column(String, index=True, unique=True, comment="企业域名")

    name = Column(String, comment="企业名称")
    short_name = Column(String, comment="简称")

    website = Column(String, comment="官网")
    desc = Column(Text, comment="备注")

    is_active = Column(Integer, default=1, server_default="1", comment="状态 1.正常 2.禁用")
    expire_at = Column(Date, comment="到期时间")

    add_user_id = Column(Integer, ForeignKey("user.id"))
    add_user = relationship("User", foreign_keys=[add_user_id])
    alt_user_id = Column(Integer, ForeignKey("user.id"))
    alt_user = relationship("User", foreign_keys=[alt_user_id])
    del_user_id = Column(Integer, ForeignKey("user.id"))

    __table_args__ = {
        "comment": "企业表",
    }
