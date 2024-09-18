from pydantic import Field

from app.core.types import Model


class UserProfileInput(Model):

    first_name: str = Field(...)
    last_name: str = Field(...)
    email: str = Field(...)
    avatar: str = Field(...)

