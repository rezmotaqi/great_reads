from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError

from app.core.settings import settings
from app.core.utils import mongo_db, hash_password


async def startup_jobs(db: Depends(mongo_db)) -> None:
    await db.users.create_index(
        [("username", 1)],
        unique=True,
        background=True,
    )
    try:
        await db.users.insert_one(
            {
                "username": settings.SUPERUSER_USERNAME,
                "password": hash_password(settings.SUPERUSER_PASSWORD),
                "is_superuser": True,
                "permissions": [],
            }
        )
        print("Superuser inserted.")
    except DuplicateKeyError:
        pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient(
        host=settings.MONGO_HOST,
        port=settings.MONGO_PORT,
        username=settings.MONGO_USER,
        password=settings.MONGO_PASSWORD,
    )
    db = client[settings.MONGO_DB]
    app.state.mongo_db = db  # type: ignore
    await startup_jobs(db)
    yield

    client.close()
