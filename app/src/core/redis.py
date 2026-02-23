from redis.asyncio import Redis

from app.src.core.config import config


class RedisClient:
    """A client for interacting with Redis cache."""

    def __init__(
        self, host: str, port: int, username: str, password: str, expire_time: int
    ):
        """
        Args:
            host (str): The hostname of the Redis server.
            port (int): The port number of the Redis server.
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.redis = Redis(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
        )
        self.__expire_time = expire_time

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.redis.close()

    async def close(self):
        """Close the Redis connectioTypeError: object bool can't be used in 'await' expressionn."""
        await self.redis.close()

    async def set(self, key, value):
        """
        Set a key-value pair in Redis.

        """
        await self.redis.set(key, value, ex=self.__expire_time)

    async def get(self, key):
        """
        Get a value from Redis by key.

        Args:
            key (str): The key to retrieve.

        """
        value: str = await self.redis.get(key)
        if value and value.isdigit():
            return int(value)
        return value

    async def clear_all(self):
        """Clear all keys and values from the Redis database."""
        await self.redis.flushall()

    async def delete(self, key: str) -> None:
        await self.redis.delete(key)


def get_redis_client(ttl: int):
    def wrapper():
        return RedisClient(
            host=config.redis.REDIS_HOST,
            port=config.redis.REDIS_PORT,
            username=config.redis.REDIS_USER,
            password=config.redis.REDIS_USER_PASSWORD,
            expire_time=ttl,
        )

    return wrapper
