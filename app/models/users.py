from typing import Optional

from pydantic import BaseModel, Field

from app.core.enums import UserStatus


class UserProfile(BaseModel):
    avatar: Optional[str]
    first_name: str
    last_name: str


class User(BaseModel):
    profile: UserProfile
    username: str
    password: str
    status: UserStatus = Field(default=UserStatus.ACTIVE)
    permissions: list[str] = Field(default_factory=list[str])

    class Config:
        extra = "ignore"
