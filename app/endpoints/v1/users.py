from fastapi import APIRouter, Depends

from app.repositories.users import UserRepository, get_user_repository
from app.schemas.users import CreateUserInput, CreateUserOutput

router = APIRouter()


@router.post("/")
async def create_user(
    data: CreateUserInput,
    user_repository: UserRepository = Depends(get_user_repository),
) -> CreateUserOutput:
    return await user_repository.create_user(data)
