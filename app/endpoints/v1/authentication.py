from typing import Any

from fastapi import APIRouter, Depends

from app.core.authentication import AuthService, get_current_user_from_database
from app.schemas.users import UserRegistrationInput, LoginInput

router = APIRouter()


@router.post("/register")
async def register(user: UserRegistrationInput, auth_service: AuthService = Depends()):
    access_token = await auth_service.register_user(user)
    return {"access_token": access_token}


@router.post("/login")
async def login(user: Any = Depends(), auth_service: AuthService = Depends()):
    access_token = await auth_service.login_user(user)
    return {"access_token": access_token}


@router.get("/me")
async def read_users_me(current_user: LoginInput = Depends(get_current_user_from_database)):
    return current_user
