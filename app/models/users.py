from typing import Optional

from pydantic import Field

from app.core.enums import UserStatus
from app.core.types import Model
from app.schemas.authentication import Role


class UserProfile(Model):
    avatar: Optional[str]
    first_name: str
    last_name: str


class User(Model):

    profile: UserProfile
    username: str
    password: str
    status: UserStatus = Field(default=UserStatus.ACTIVE)
    permissions: list[str] = Field(default_factory=list[str])
    role: Role = Field(...)
