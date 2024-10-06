from fastapi import APIRouter

from app.endpoints.v1.books import router as books_router
from app.endpoints.v1.authentication import router as authentication_router

router = APIRouter()


router.include_router(books_router, prefix="/book", tags=["books"])
router.include_router(
    authentication_router, prefix="/authentication", tags=["authentication"]
)
