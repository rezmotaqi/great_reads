from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.users import User
from app.schemas.users import UserRegistrationInput


class UserRepository:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.db = db

    async def create_user(self, user_registration_input: UserRegistrationInput, hashed_password: str) -> None:
        user = User.model_validate({**user_registration_input.model_dump(), "password": hashed_password})
        await self.db.users.insert_one(user.model_dump())

    async def get_user_by_email(self, email: str):
        return await self.db.users.find_one({"username": email})

    async def get_user_by_id(self, user_id: ObjectId) -> User:
        return await self.db.users.find_one({"_id": user_id})
