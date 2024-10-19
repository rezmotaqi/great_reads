import datetime

from pydantic import Field

from app.core.enums import UserStatus
from app.core.types import Model
from app.schemas.authentication import Role


class UserProfile(Model):
    avatar: str | None = None
    first_name: str
    last_name: str


class User(Model):

    profile: UserProfile | None = None
    username: str
    password: str
    status: UserStatus = Field(default=UserStatus.ACTIVE)
    permissions: list[str] | None = None
    role: Role | None = None
    created_at: datetime.datetime = Field()
    updated_at: datetime.datetime | None = None
