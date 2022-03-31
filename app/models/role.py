"""Role Model."""
from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Role(Base):
    """角色"""

    company_id = Column(Integer, ForeignKey("company.id"), comment="企业id", index=True)
    company = relationship("Company", foreign_keys=[company_id])

    code = Column(String, comment="唯一编码", index=True)
    name = Column(String, comment="企业名称")

    sort = Column(Integer, comment="顺序", default=100, server_default="100")
    remark = Column(String, comment="备注")

    status = Column(Integer, comment="状态 1.正常 2.禁用", default=1, server_default="1")

    dataScopeType = Column(
        Integer,
        comment="授权范围 1.仅本人数据 2.本部门数据 3.本部门及以下数据 4.全部数据 5.自定义数据",
        default=1,
        server_default="1",
    )

    __table__args__ = {
        "comment": "角色",
    }


class RoleAccess(Base):
    """角色权限"""

    role_id = Column(Integer, ForeignKey("role.id"), comment="角色id", index=True)
    role = relationship("Role", foreign_keys=[role_id])
    access_id = Column(Integer, ForeignKey("access.id"), comment="权限id", index=True)
    access = relationship("Access", foreign_keys=[access_id])

    __table__args__ = {
        "comment": "角色权限",
    }


class RoleDataScope(Base):
    """角色数据范围"""

    role_id = Column(Integer, ForeignKey("role.id"), comment="角色id", index=True)
    role = relationship("Role", foreign_keys=[role_id])
    org_id = Column(Integer, ForeignKey("org.id"), comment="组织id", index=True)
    org = relationship("Org", foreign_keys=[org_id])

    __table__args__ = {
        "comment": "角色数据范围",
    }
