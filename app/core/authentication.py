from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import jwt
from starlette import status

from app.config.settings import settings
from app.models.users import User
from app.repositories.users import UserRepository
from app.schemas.users import UserRegistrationInput, LoginInput
from utils import hash_password, generate_jwt_token, check_password


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register_user(self, user_registration_input: UserRegistrationInput) -> None:
        # if not validate_email(user_data.email):
        #     raise HTTPException(status_code=400, detail="Invalid email")
        # if not validate_password(user_data.password):
        #     raise HTTPException(status_code=400, detail="Invalid password")

        # existing_user = await self.user_repository.get_user_by_email(user_data.email)
        # if existing_user:
        #     raise HTTPException(status_code=400, detail="User already exists")

        hashed_password = hash_password(user_registration_input.password)

        await self.user_repository.create_user(user_registration_input, hashed_password=hashed_password)

    async def login_user(self, user_data: LoginInput):
        user = await self.user_repository.get_user_by_email(user_data.email)
        if not user or not check_password(user_data.password, user.password):
            raise HTTPException(status_code=401, detail="Unauthorized")

        # Generate JWT token
        access_token = generate_jwt_token(user.id)
        return access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # For demonstration purposes


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

        # Check if the JTI is blacklisted in Redis

        if redis_client.sismember("jti_blacklist", payload["jti"]):

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is revoked",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # You can fetch user details from a database here based on payload["sub"]
        user = UserRepository(db=db).get_user_by_id(user_id=payload["sub"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Example usage in a FastAPI endpoint
@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
