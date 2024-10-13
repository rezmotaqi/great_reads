import logging
from datetime import datetime

import pymongo
from bson import ObjectId
from fastapi import Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from starlette import status

from app.core.utils import get_app_state_mongo_db
from app.models.users import User
from app.schemas.authentication import ReaderRole, Role
from app.schemas.users import UserRegistrationInput


class UserRepository:
    db: AsyncIOMotorDatabase

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def create_user(
        self,
        user_registration_input: UserRegistrationInput,
        hashed_password: str,
        role: Role = ReaderRole(),
    ) -> None:
        now = datetime.utcnow()
        user = User.model_validate(
            {
                **user_registration_input.model_dump(),
                "password": hashed_password,
                "created_at": now,
                "updated_at": now,
                "permissions": await self.generate_permissions(role=role),
            }
        )
        print(user.model_dump())
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

    @staticmethod
    async def get_user_by_id(user_id: ObjectId):

        return await get_app_state_mongo_db().users.find_one(
            {"_id": ObjectId(user_id)}
        )

    @staticmethod
    async def get_permissions(user_id: ObjectId) -> list:
        user = await get_app_state_mongo_db().users.find_one(
            {"_id": user_id}, {"permissions": 1}
        )

        return user.get("permissions", [])

    @staticmethod
    async def generate_permissions(role: Role = ReaderRole()) -> list:
        return role.permissions


async def get_user_repository(
    db: AsyncIOMotorDatabase = Depends(get_app_state_mongo_db),
) -> UserRepository:
    a = UserRepository(db)
    print(
        a.get_permissions(user_id=ObjectId("670a5ecd19dc393be2aafa57")),
        "1" * 100,
    )
    return a
