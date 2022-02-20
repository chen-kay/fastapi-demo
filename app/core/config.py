from pathlib import Path
from typing import Optional

from pydantic import BaseSettings

SQLITE_DATABASE_URL = "sqlite:///db.sqlite3?check_same_thread=False"


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
    SECRET_KEY: str = (
        "oa7iYpGp3BvGmwKYondTU2U-IN0njhW0aXGbqyYmflQ"  # secrets.token_urlsafe(32)
    )

    # 项目根路径
    BASE_PATH: Path = Path(__file__).resolve().parent.parent.parent

    DEFAULT_PAGE_SIZE: int = 100

    # mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8
    SQLALCHEMY_DATABASE_URL: Optional[str] = SQLITE_DATABASE_URL
    # redis://:{password}@{host}:{port}/{db}?charset=utf8
    REDIS_URL: Optional[str] = None

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
