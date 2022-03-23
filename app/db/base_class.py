from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.sql import func


@as_declarative()
class Base:
    # 通用的字段
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    is_del = Column(
        Integer,
        default=0,
        server_default="0",
        comment="逻辑删除:0=未删除,1=删除",
    )
    add_at = Column(
        DateTime,
        default=datetime.now,
        server_default=func.now(),
        comment="创建时间",
    )
    alt_at = Column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        server_default=func.now(),
        server_onupdate=func.now(),
        comment="更新时间",
    )
    add_user = Column(
        String,
        comment="创建人",
        default="",
        server_default="",
        index=True,
    )
    alt_user = Column(
        String,
        comment="修改人",
        default="",
        server_default="",
        index=True,
    )

    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        import re

        # 如果没有指定__tablename__  则默认使用model类名转换表名字
        name_list = re.findall(r"[A-Z][a-z\d]*", cls.__name__)
        # 表名格式替换成 下划线_格式 如 MallUser 替换成 mall_user
        return "_".join(name_list).lower()
