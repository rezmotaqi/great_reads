import logging
from datetime import datetime

import pymongo
from bson import ObjectId
from fastapi import HTTPException
from starlette import status

from app.core.utils import mongo_db
from app.models.users import User
from app.schemas.authentication import ReaderRole, Role
from app.schemas.users import (
    CreateUserInput,
    UserRegistrationInput,
    CreateUserOutput,
)


class UserRepository:
    @staticmethod
    async def create_user(data: CreateUserInput) -> CreateUserOutput:
        """This method is used by superuser to create a user."""
        data = User.model_validate(
            {
                **data.model_dump(mode="json"),
                "password": data.password.get_secret_value(),
            }
        )
        try:
            await mongo_db().users.insert_one(data.model_dump())
            return CreateUserOutput.model_validate(data.model_dump())
        except pymongo.errors.DuplicateKeyError:  # type: ignore
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists",
            )

    async def register_user(
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
                "permissions": await self.generate_permissions(),
            }
        )
        print(user.model_dump())
        try:
            await mongo_db().users.insert_one(user.model_dump())
        except pymongo.errors.DuplicateKeyError:  # type: ignore

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists",
            )
        except Exception as e:
            logging.log(logging.CRITICAL, e)
            raise e

    @staticmethod
    async def get_user_by_username(username: str):
        return await mongo_db().users.find_one({"username": username})

    @staticmethod
    async def get_user_by_id(user_id: ObjectId):

        return await mongo_db().users.find_one({"_id": ObjectId(user_id)})

    @staticmethod
    async def get_permissions(user_id: ObjectId) -> list:
        user = await mongo_db().users.find_one(
            {"_id": user_id}, {"permissions": 1}
        )

        return user.get("permissions", [])

    @staticmethod
    async def generate_permissions(role: Role = ReaderRole()) -> list:
        return role.permissions


async def get_user_repository() -> UserRepository:
    return UserRepository()
