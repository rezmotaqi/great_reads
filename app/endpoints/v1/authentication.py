from typing import Any

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.core.authentication import (
    AuthService,
    get_authentication_service,
    get_current_user_from_database,
)
from app.schemas.users import (
    LoginInput,
    UserRegistrationInput,
    UserRegistrationOutput,
)

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user: UserRegistrationInput,
    auth_service: AuthService = Depends(get_authentication_service),
):
    await auth_service.register_user(user)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=UserRegistrationOutput,
    )


@router.get("/me")
async def read_users_me(
    current_user: LoginInput = Depends(get_current_user_from_database),
):
    return current_user


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    user: Any = Depends(get_current_user_from_database),
    auth_service: AuthService = Depends(get_authentication_service),
):
    await auth_service.login_user(user)
