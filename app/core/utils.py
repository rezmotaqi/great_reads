import bcrypt
from motor.motor_asyncio import AsyncIOMotorDatabase


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(
                *args, **kwargs
            )
        return cls._instances[cls]


def return_app_instance():
    from app.main import app

    return app


# noinspection PyUnresolvedReferences
def mongo_db() -> AsyncIOMotorDatabase:
    app = return_app_instance()
    return app.state.mongo_db


def hash_password(password: str) -> str:
    """Hashes a password using bcrypt.

    Args:
      password (str): The password to hash.

    Returns:
      str: The hashed password.

    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")
