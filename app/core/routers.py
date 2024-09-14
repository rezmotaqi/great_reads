from fastapi import APIRouter

from app.endpoints.books import router as books_router

router = APIRouter()


router.include_router(books_router, prefix="/book", tags=["books"])

