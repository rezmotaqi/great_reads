from datetime import datetime

from bson import ObjectId
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.enums import UserStatuses
from app.handlers.databases import get_mongo_db
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
            }
        )
        await self.db.users.insert_one(user.model_dump())

    async def get_user_by_email(self, email: str):
        return await self.db.users.find_one({"username": email})

    async def get_user_by_id(self, user_id: ObjectId):
        return await self.db.users.find_one({"_id": user_id})

    async def get_permissions(self, user_id: ObjectId) -> list:
        return await self.db.users.find_one(
            {
                "_id": user_id,
                "status": UserStatuses.ACTIVE,
            }
        )


def get_user_repository(
    db: AsyncIOMotorDatabase = Depends(get_mongo_db),
) -> UserRepository:
    return UserRepository(db=db)
