__all__ = ('cache', )


from redis.asyncio.client import Redis
from redis.asyncio.connection import ConnectionPool

from conf import settings

from .client import RedisClientWrapper


connection_pool = ConnectionPool.from_url(settings.REDIS_URL)
redis = Redis(connection_pool=connection_pool)

cache: RedisClientWrapper = RedisClientWrapper(redis)
