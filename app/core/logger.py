import os
import time

from app.core.config import settings
from loguru import logger

# 定位到log日志文件
log_path = os.path.join(settings.BASE_PATH, "logs")

if not os.path.exists(log_path):
    os.mkdir(log_path)

log_path = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}.log')

logger.add(
    log_path,
    rotation="500 MB",
    encoding="utf-8",
    enqueue=True,
    level="ERROR",
)

__all__ = ["logger"]
