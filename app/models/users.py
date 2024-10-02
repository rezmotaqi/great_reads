from typing import Optional

from pydantic import BaseModel


class UserProfile(BaseModel):
    avatar: Optional[str]
    first_name: str
    last_name: str


class User(BaseModel):
    profile: UserProfile
    username: str
    password: str

    class Config:
        extra = 'ignore'
