from app.core.utils import mongo_db
from app.models.books import BookModel
from app.schemas.books import BookCreateInput, BookCreateOutput


class Book:
    @staticmethod
    async def save(data: BookCreateInput) -> BookCreateOutput:
        model = BookModel.model_validate(data.model_dump())
        result = await mongo_db().books.insert_one(model.model_dump())
        return BookCreateOutput(
            **model.model_dump(), book_id=result.inserted_id
        )
