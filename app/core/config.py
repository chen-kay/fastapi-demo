from pathlib import Path
from typing import Optional

from pydantic import BaseSettings

SQLITE_DATABASE_URI = "sqlite:///db.sqlite3?check_same_thread=False"


class Settings(BaseSettings):
    DEBUG: bool = True
    TITLE: str = "FastAPI Demo"
    DESCRIPTION: str = "FastAPI"
    # 文档地址 默认为docs
    DOCS_URL: str = "/api/docs"
    # 文档关联请求数据接口
    OPENAPI_URL: str = "/api/openapi.json"
    # redoc 文档
    REDOC_URL: Optional[str] = "/api/redoc"

    # token过期时间 分钟
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # 生成token的加密算法
    ALGORITHM: str = "HS256"
    # secrets.token_urlsafe(32)
    SECRET_KEY: str = "oa7iYpGp3BvGmwKYondTU2U-IN0njhW0aXGbqyYmflQ"

    # 项目根路径
    BASE_PATH: Path = Path(__file__).resolve().parent.parent.parent

    DEFAULT_PAGE_SIZE: int = 100

    # 默认管理员账号密码等信息
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin"
    ADMIN_NICKNAME: str = "admin"
    ADMIN_EMAIL: str = "l1328076914@gmail.com"

    DATABASE_NAME: str = "fastapi_demo"
    # mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8
    DATABASE_URI: Optional[str] = SQLITE_DATABASE_URI
    SQLALCHEMY_DATABASE_URI: Optional[str] = SQLITE_DATABASE_URI
    # redis://:{password}@{host}:{port}/{db}?charset=utf8
    REDIS_URL: Optional[str] = None

    FIRST_SUPERDOMAIN:str = 'system'
    FIRST_SUPERUSER: str = "admin"
    FIRST_SUPERUSER_PASSWORD: str = "admin"
    FIRST_ADMINUSER:str = 'admin'
    FIRST_ADMIN_PASSWORD: str = '123456'

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
