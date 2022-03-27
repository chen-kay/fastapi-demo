"""Log Model."""
from app.db.base_class import Base
from sqlalchemy import Column, DateTime, Integer, String, Text


class VisitLog(Base):
    """访问日志
    visType: 1.登录 2.登出
    """

    account = Column(String, comment="访问用户", index=True)

    name = Column(String, comment="日志名称")
    visType = Column(Integer, comment="访问类型", index=True)

    userAgent = Column(String, comment="用户代理")
    browser = Column(String, comment="浏览器")
    os = Column(String, comment="操作系统")
    ip = Column(String, comment="IP地址")
    location = Column(String, comment="地址")

    message = Column(String, comment="消息")
    success = Column(String, comment="是否成功", index=True)

    visTime = Column(DateTime, comment="访问时间", index=True)


class OperateLog(Base):
    """操作日志
    visType: 0.其他 1.增加 2.删除 3.更新 4.查询 5.详情 6.修改状态 7.清空 8.授权 9.导入 10.导出
    """

    account = Column(String, comment="操作人", index=True)

    name = Column(String, comment="日志名称")
    opType = Column(Integer, comment="操作类型", index=True)

    className = Column(String, comment="api模块")
    methodName = Column(String, comment="api方法")

    url = Column(String, comment="请求url")
    param = Column(Text, comment="请求参数")
    reqMethod = Column(Text, comment="请求方法")
    authorization = Column(String, comment="认证请求头")
    # signValue = Column(String, comment="签名")

    userAgent = Column(String, comment="用户代理")
    browser = Column(String, comment="浏览器")
    os = Column(String, comment="操作系统")
    ip = Column(String, comment="IP地址")
    location = Column(String, comment="地址")

    result = Column(Text, comment="返回信息")
    message = Column(String, comment="消息")
    success = Column(String, comment="是否成功", index=True)

    opTime = Column(DateTime, comment="操作时间", index=True)
