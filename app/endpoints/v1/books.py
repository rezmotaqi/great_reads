from fastapi import APIRouter

from app.repositories.books import Book
from app.schemas.books import BookCreateInput, BookCreateOutput

router = APIRouter()


# @router.get("/", response_model=List[Book])


@router.post("/", response_model=BookCreateOutput)
async def create_book(data: BookCreateInput):
    book = await Book().save(data=data)
    return book
