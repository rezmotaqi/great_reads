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

    class Config:
        extra = "ignore"
