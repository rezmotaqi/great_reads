from typing import Any

from fastapi import APIRouter, Depends, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.authentication import (
    AuthService,
    get_current_user_from_database,
    get_authentication_service,
)
from app.handlers.databases import get_mongo_db
from app.schemas.users import LoginInput, UserRegistrationInput

router = APIRouter()


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=None
)
async def register(
    user: UserRegistrationInput,
    auth_service: AuthService = Depends(get_authentication_service),
):
    ...
    await auth_service.register_user(user)


@router.get("/me")
async def read_users_me(
    current_user: LoginInput = Depends(get_current_user_from_database),
):
    return current_user


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    user: Any = Depends(),
    # auth_service: AuthService = Depends(get_authentication_service),
):
    ...
    # await auth_service.login_user(user)
