from fastapi import Depends

from app.handlers.databases import get_mongo_db
from app.models.books import BookModel
from app.schemas.books import BookCreateInput, BookCreateOutput


class Book:
    def __init__(self, db: Depends(get_mongo_db)) -> None:
        self.db = db

    async def save(self, data: BookCreateInput) -> BookCreateOutput:
        model = BookModel.model_validate(data.model_dump())
        result = await self.db.books.insert_one(model.model_dump())
        return BookCreateOutput(**model.model_dump(), book_id=result.inserted_id)
