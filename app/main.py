

from fastapi import FastAPI
from app.core.routers import router
from app.config.settings import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION
)

app.include_router(router=router, prefix=f"{settings.API_ROUTE_PREFIX}{settings.VERSION_ROUTE_PREFIX}")


