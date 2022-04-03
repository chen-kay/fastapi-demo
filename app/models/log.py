"""Log Model."""
from app.db.session import Base
from sqlalchemy import Column, DateTime, Integer, String, Text


class VisitLog(Base):
    """访问日志
    visType: 1.登录 2.登出
    """
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    account = Column(String(50), comment="访问用户", index=True)

    name = Column(String(50), comment="日志名称")
    visType = Column(Integer, comment="访问类型", index=True)

    userAgent = Column(String(200), comment="用户代理")
    browser = Column(String(50), comment="浏览器")
    os = Column(String(50), comment="操作系统")
    ip = Column(String(50), comment="IP地址")
    location = Column(String(50), comment="地址")

    message = Column(String(100), comment="消息")
    success = Column(String(50), comment="是否成功", index=True)

    visTime = Column(DateTime, comment="访问时间", index=True)

    __tablename__ = "visit_log"


class OperateLog(Base):
    """操作日志
    visType: 0.其他 1.增加 2.删除 3.更新 4.查询 5.详情 6.修改状态 7.清空 8.授权 9.导入 10.导出
    """
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    account = Column(String(50), comment="操作人", index=True)

    name = Column(String(50), comment="日志名称")
    opType = Column(Integer, comment="操作类型", index=True)

    className = Column(String(50), comment="api模块")
    methodName = Column(String(50), comment="api方法")

    url = Column(String(200), comment="请求url")
    param = Column(Text, comment="请求参数")
    reqMethod = Column(Text, comment="请求方法")
    authorization = Column(String(200), comment="认证请求头")
    # signValue = Column(String, comment="签名")

    userAgent = Column(String(200), comment="用户代理")
    browser = Column(String(50), comment="浏览器")
    os = Column(String(50), comment="操作系统")
    ip = Column(String(50), comment="IP地址")
    location = Column(String(50), comment="地址")

    result = Column(Text, comment="返回信息")
    message = Column(String(100), comment="消息")
    success = Column(String(50), comment="是否成功", index=True)

    opTime = Column(DateTime, comment="操作时间", index=True)

    __tablename__ = "operate_log"
