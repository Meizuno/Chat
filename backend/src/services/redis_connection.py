import redis.asyncio as redis
from src.config import REDIS_URL


async def get_redis() -> redis.Redis:
    """Get redis connection"""

    return redis.from_url(REDIS_URL, decode_responses=True)
