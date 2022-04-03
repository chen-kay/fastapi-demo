"""Role Model."""
from app.db.session import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship


class Role(Base):
    """角色"""

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    company_id = Column(Integer, ForeignKey("company.id"), comment="企业id", index=True)
    company = relationship("Company", foreign_keys=[company_id])

    code = Column(String(50), comment="唯一编码", index=True)
    name = Column(String(50), comment="企业名称")

    sort = Column(Integer, comment="顺序", default=100, server_default="100")
    remark = Column(Text, comment="备注")

    status = Column(Integer, comment="状态 1.正常 2.禁用", default=1, server_default="1")

    dataScopeType = Column(
        Integer,
        comment="授权范围 1.仅本人数据 2.本部门数据 3.本部门及以下数据 4.全部数据 5.自定义数据",
        default=1,
        server_default="1",
    )

    __tablename__ = "role"
    __table__args__ = {
        "comment": "角色",
    }


class RoleAccess(Base):
    """角色权限"""

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    role_id = Column(Integer, ForeignKey("role.id"), comment="角色id", index=True)
    role = relationship("Role", foreign_keys=[role_id])
    access_id = Column(Integer, ForeignKey("access.id"), comment="权限id", index=True)
    access = relationship("Access", foreign_keys=[access_id])

    __tablename__ = "role_access"
    __table__args__ = {
        "comment": "角色权限",
    }


class RoleDataScope(Base):
    """角色数据范围"""

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    role_id = Column(Integer, ForeignKey("role.id"), comment="角色id", index=True)
    role = relationship("Role", foreign_keys=[role_id])
    org_id = Column(Integer, ForeignKey("org.id"), comment="组织id", index=True)
    org = relationship("Org", foreign_keys=[org_id])

    __tablename__ = "role_data_scope"
    __table__args__ = {
        "comment": "角色数据范围",
    }
