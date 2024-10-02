import aioredis
from motor.motor_asyncio import AsyncIOMotorClient

from app.config.settings import settings


class MongoHandler:
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
        return client[settings.MONGO_DB]


def get_db():
    """A function that returns database object."""
    return MongoHandler.get_database()


class RedisHandler:
    redis_client = aioredis.from_url(REDIS_URL)
