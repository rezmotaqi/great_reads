from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.settings import settings
from app.core.utils import get_app_state_mongo_db


async def startup_jobs(db: Depends(get_app_state_mongo_db)) -> None:
    db.users.create_index(
        [("username", 1)],
        unique=True,
        background=True,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient(
        host=settings.MONGO_HOST,
        port=settings.MONGO_PORT,
        username=settings.MONGO_USER,
        password=settings.MONGO_PASSWORD,
    )
    db = client[settings.MONGO_DB]
    app.state.mongo_db = db
    await startup_jobs(db)
    yield

    client.close()
