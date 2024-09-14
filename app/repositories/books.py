from dataclasses import dataclass

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.books import BookModel
from app.schemas.books import BookPostInput


@dataclass
class Book:
    book_data: BookPostInput
    db: AsyncIOMotorDatabase

    async def prepare_book_model(self):
        return BookModel(**self.book_data.model_dump())

    async def save(self):
        model = await self.prepare_book_model()
        await self.db.books.insert_one(model.model_dump())
