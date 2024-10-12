from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.utils import get_app_state_mongo_db
from app.models.books import BookModel
from app.schemas.books import BookCreateInput, BookCreateOutput


class Book:
    def __init__(
        self, db: AsyncIOMotorDatabase = Depends(get_app_state_mongo_db)
    ) -> None:
        self.db = db

    async def save(self, data: BookCreateInput) -> BookCreateOutput:
        model = BookModel.model_validate(data.model_dump())
        result = await self.db.books.insert_one(model.model_dump())
        return BookCreateOutput(
            **model.model_dump(), book_id=result.inserted_id
        )
