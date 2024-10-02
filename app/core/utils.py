import uuid
from datetime import datetime, timedelta
from typing import Any

import bcrypt
from jwt import jwt

from app.config.settings import settings


def hash_password(password: str) -> str:
    """Hashes a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
            return cls._instances[cls]


def check_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def generate_jwt_token(user_id: int) -> str:
    now = datetime.now(datetime.UTC)
    token_expire = now + timedelta()
    jwt_payload = {
        "sub": user_id,
        "exp": token_expire,
        "iat": now,
        "jti": str(uuid.uuid4()),
    }
    access_token = jwt.encode(jwt_payload, settings.SECRET_KEY, algorithm="HS256")
    return access_token


