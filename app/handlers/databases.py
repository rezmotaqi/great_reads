import redis.asyncio as redis
from motor.motor_asyncio import AsyncIOMotorClient

from app.config.settings import settings
from app.core.utils import SingletonMeta


class MongoHandler(metaclass=SingletonMeta):
    _client: AsyncIOMotorClient = None

    @classmethod
    def get_client(cls) -> AsyncIOMotorClient:
        if cls._client is None:
            cls._client = AsyncIOMotorClient(
                host=settings.MONGO_HOST,
                port=settings.MONGO_PORT,
                username=settings.MONGO_USER,
                password=settings.MONGO_PASSWORD,
            )
        return cls._client

    @classmethod
    def get_database(cls):
        client = cls.get_client()
        try:
            yield client[settings.MONGO_DB]
        finally:
            client.close()


def get_mongo_db():
    """A function that returns database object."""
    return MongoHandler.get_database()


class RedisHandler(metaclass=SingletonMeta):
    redis_client = redis.from_url(settings.REDIS_URL)
