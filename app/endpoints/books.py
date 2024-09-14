from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.handlers.mongo import get_db
from app.repositories.books import Book
from app.schemas.books import BookPostInput

router = APIRouter()


# @router.get("/", response_model=List[Book])

@router.post("", response_model=BookPostInput)
async def create_book(book: BookPostInput, db: AsyncIOMotorDatabase = Depends(get_db)):
    book = Book(book_data=book, db=db).save()
    return book
