from dataclasses import dataclass

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.books import BookModel
from app.schemas.books import BookCreateInput, BookCreateOutput


@dataclass
class Book:
    db: AsyncIOMotorDatabase

    async def save(self, data: BookCreateInput) -> BookCreateOutput:
        model = await BookModel.model_validate(data.model_dump())
        result = await self.db.books.insert_one(model.model_dump())
        return BookCreateOutput(**model.model_dump(), id=result.inserted_id)
