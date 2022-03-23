from app.core.config import settings
from loguru import logger

# 定位到log日志文件
log_path = settings.BASE_PATH / "logs"

if not log_path.exists():
    log_path.mkdir(parents=True)

log_file = log_path / f"access.log"

logger.add(
    log_file,
    rotation="100 MB",
    retention="3 days",
    encoding="utf-8",
    enqueue=True,
    level="ERROR",
)

__all__ = ["logger"]
