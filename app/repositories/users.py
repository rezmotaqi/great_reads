import logging
from datetime import datetime

import pymongo
from bson import ObjectId
from fastapi import Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from starlette import status

from app.core.authentication import generate_user_permissions
from app.core.enums import UserStatus
from app.core.utils import get_app_state_mongo_db
from app.models.users import User
from app.schemas.users import UserRegistrationInput


class UserRepository:
    db: AsyncIOMotorDatabase

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def create_user(
        self,
        user_registration_input: UserRegistrationInput,
        hashed_password: str,
    ) -> None:
        now = datetime.utcnow()
        user = User.model_validate(
            {
                **user_registration_input.model_dump(),
                "password": hashed_password,
                "created_at": now,
                "updated_at": now,
                "prs": await generate_user_permissions(),
            }
        )
        try:
            await self.db.users.insert_one(user.model_dump())
        except pymongo.errors.DuplicateKeyError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists",
            )
        except Exception as e:
            logging.log(logging.CRITICAL, e)
            raise e

    async def get_user_by_username(self, username: str):
        return await self.db.users.find_one({"username": username})

    async def get_user_by_id(self, user_id: ObjectId):

        return await self.db.users.find_one({"_id": user_id})

    async def get_permissions(self, user_id: ObjectId) -> list:

        return await self.db.users.find_one(
            {
                "_id": user_id,
                "status": UserStatus.ACTIVE,
            }
        )


async def get_user_repository(
    db: AsyncIOMotorDatabase = Depends(get_app_state_mongo_db),
) -> UserRepository:
    a = UserRepository(db)
    await a.get_permissions()
    return UserRepository(db=db)
