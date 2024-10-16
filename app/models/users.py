import datetime
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
    permissions: Optional[list[str]] = None
    role: Optional[Role] = None
    created_at: datetime.datetime = Field()
    updated_at: Optional[datetime.datetime] = Field()
