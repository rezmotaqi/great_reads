import redis.asyncio as redis
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.settings import settings
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
    def get_database(cls) -> AsyncIOMotorDatabase:
        client = cls.get_client()
        return client[settings.MONGO_DB]


def get_mongo_db() -> AsyncIOMotorDatabase:
    """A function that returns database object."""
    return MongoHandler.get_database()


class RedisHandler(metaclass=SingletonMeta):
    redis_client = redis.from_url(settings.REDIS_URL)
