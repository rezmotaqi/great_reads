import json
import uuid
from datetime import datetime, timedelta

import bcrypt
from bson import ObjectId
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose import ExpiredSignatureError, JWTError  # Import exceptions
from motor.motor_asyncio import AsyncIOMotorDatabase
from starlette import status

from app.config.settings import settings
from app.core.utils import SingletonMeta
from app.handlers.databases import get_mongo_db
from app.models.users import User
from app.repositories.users import UserRepository
from app.schemas.users import JwtExtractedUser, LoginInput, UserRegistrationInput


def hash_password(password: str) -> str:
    """Hashes a password subng bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


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

        access_token = generate_jwt_token(user.id)
        return access_token


async def get_current_user_from_database(
        token: str = Depends(OAuth2PasswordBearer(tokenUrl="/login")),
        db: AsyncIOMotorDatabase = Depends(get_mongo_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user: User = await UserRepository(db=db).get_user_by_id(user_id=ObjectId(user_id))
        if not user:
            raise credentials_exception
        return user
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:  # Catch any jose JWT errors
        raise credentials_exception


def check_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def generate_jwt_token(user_id: int) -> str:
    now = datetime.utcnow()
    token_expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    jwt_payload = {
        "sub": str(user_id),  # Ensure user_id is a string
        "exp": token_expire,
        "iat": now,
        "jti": str(uuid.uuid4()),
    }
    access_token = jwt.encode(jwt_payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return access_token


async def get_user_jwt_payload_data_from_token(token: str) -> JwtExtractedUser:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        return JwtExtractedUser(user_id=int(user_id), permissions=payload.get("permissions", []))
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


class PermissionManager(metaclass=SingletonMeta):
    """
    Manages permissions for API endpoints from a JSON file.

    This class uses the singleton pattern to ensure only one instance exists.
    It loads permissions from a JSON file and provides methods to retrieve
    and modify them.

    Attributes:
        permissions (dict): Dictionary holding the endpoint permissions loaded from the JSON file.

    Example:
         permission_manager = PermissionManager()
         permissions = permission_manager.get_permissions("/users", "GET")
    """

    def __init__(self):
        self.load_permissions()
        self.permissions = None

    def load_permissions(self):
        """
        Loads endpoint permissions from the 'permissions.json' file.
        """
        with open("permissions.json", "r") as f:
            self.permissions = json.load(f)

    def get_endpoint_permissions(self, endpoint, method):
        """
        Retrieves the required permissions for a given endpoint and HTTP method.

        Args:
            endpoint (str): The API endpoint path.
            method (str): The HTTP method (e.g., "GET", "POST").

        Returns:
            list: A list of required permissions.
        """
        endpoint_permissions: dict = self.permissions["endpoints"].get(endpoint)
        if endpoint_permissions:
            return endpoint_permissions.get(method, [])
        return []

    def edit_permissions(self, endpoint, method, new_permissions: list):
        """
        Modifies the permissions for a specific endpoint and HTTP method.

        Args:
            endpoint (str): The API endpoint path.
            method (str): The HTTP method.
            new_permissions (list): The new list of permissions.

        Raises:
            ValueError: If any of the new permissions are invalid.
        """
        valid_permissions = self.permissions["all_permissions"]
        for permission in new_permissions:
            if permission not in valid_permissions:
                raise ValueError(f"Invalid permission: {permission}")
        if endpoint not in self.permissions["endpoints"]:
            self.permissions["endpoints"][endpoint] = {}
        self.permissions["endpoints"][endpoint][method] = new_permissions
        self.save_permissions()

    def save_permissions(self):
        with open("permissions.json", "w") as f:
            json.dump(self.permissions, f, indent=4)

    def get_public_endpoints(self):
        return self.permissions["public_endpoints"]
