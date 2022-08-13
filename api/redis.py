import redis.asyncio as redis
from api.settings import settings

redis_global = None


async def init_redis():
    redis_instance = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
        db=settings.REDIS_DB,
    )
    return redis_instance
