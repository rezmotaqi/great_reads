from fastapi import APIRouter, Depends, status

from app.core.authentication import (
    AuthService,
    get_authentication_service,
)
from app.schemas.authentication import LoginInput
from app.schemas.users import (
    UserRegistrationInput,
)

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user: UserRegistrationInput,
    auth_service: AuthService = Depends(get_authentication_service),
):
    return await auth_service.register_user(user)


@router.get("/me")
async def read_users_me(
    # current_user: CompleteUserDatabaseOutput = Depends(get_current_user),
):

    return


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    data: LoginInput,
    auth_service: AuthService = Depends(get_authentication_service),
):
    await auth_service.login_user(user_data=data)
    return
