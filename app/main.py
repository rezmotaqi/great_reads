from fastapi import FastAPI

from app.core.middlewares import auth_middleware
from app.core.routers import router
from app.core.settings import settings
from app.core.startups import lifespan

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    lifespan=lifespan,
)

app.include_router(router=router, prefix=f"{settings.API_ROUTE_PREFIX}")

app.middleware("http")(auth_middleware)
