from redis.asyncio.client import Redis

from .redis_settings import RedisSettings


class RedisClient(Redis):
    def __init__(self, settings: RedisSettings) -> None:
        super().__init__(port=settings.port,
                         host=settings.host,
                         username=settings.username,
                         password=settings.password,
                         db=settings.database)
