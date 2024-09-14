from urllib.request import BaseHandler

from motor.motor_asyncio import AsyncIOMotorClient

from app.config.settings import settings
from app.utils.singleton import SingletonMeta


class MongoHandler(metaclass=SingletonMeta):
    client: AsyncIOMotorClient = AsyncIOMotorClient(host=settings.MONGO_HOST, port=settings.MONGO_PORT)
    db = client[settings.MONGO_DB]

    def get_database(self):
        return self.db


def get_db():
    mongo = MongoHandler()
    return mongo.get_database()
