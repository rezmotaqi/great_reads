from fastapi import APIRouter, Depends, status

from app.core.authentication import (AuthService, get_authentication_service,
                                     get_current_user)
from app.schemas.users import CurrentUser, LoginInput, UserRegistrationInput

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user: UserRegistrationInput,
    auth_service: AuthService = Depends(get_authentication_service),
):
    return await auth_service.register_user(user)


@router.get("/me", response_model=CurrentUser)
async def logged_in_user(
    current_user: CurrentUser = Depends(get_current_user),
) -> CurrentUser:

    return current_user


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    data: LoginInput,
    auth_service: AuthService = Depends(get_authentication_service),
):
    access_token = await auth_service.login_user(user_data=data)

    return {"access_token": access_token}
