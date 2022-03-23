"""User Model."""
from app.db.base_class import Base
from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    """用户"""

    company_id = Column(Integer, ForeignKey("company.id"))
    company = relationship("Company", foreign_keys=[company_id])
    org_id = Column(Integer, ForeignKey("org.id"))
    org = relationship("Org", foreign_keys=[org_id])

    username = Column(String, comment="账号", index=True)
    fullname = Column(String, comment="姓名")

    nickname = Column(String, comment="昵称")

    hashed_password = Column(String, comment="密码")

    birth = Column(Date, comment="生日")
    sex = Column(Integer, comment="性别 0.无 1.男 2.女", default=0, server_default="0")

    email = Column(String, comment="邮箱")
    mobile = Column(String, comment="手机号")

    status = Column(Integer, comment="状态 1.正常 2.禁用", default=1, server_default="1")
    is_admin = Column(Integer, comment="管理员 1.是 0.否", default=0, server_default="0")
    is_superuser = Column(
        Integer,
        comment="系统管理员 1.是 0.否",
        default=0,
        server_default="0",
    )

    __table__args__ = {
        "comment": "用户",
    }


class UserRole(Base):
    """用户角色"""

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", foreign_keys=[user_id])
    role_id = Column(Integer, ForeignKey("role.id"))
    role = relationship("Role", foreign_keys=[role_id])

    __table__args__ = {
        "comment": "用户角色",
    }
