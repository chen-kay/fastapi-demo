from typing import Optional

from aioredis import Redis, from_url
from app.core.config import settings


async def get_redis_pool() -> Optional[Redis]:
    if not settings.REDIS_URL:
        return None
    return from_url(settings.REDIS_URL, decode_responses=True)
