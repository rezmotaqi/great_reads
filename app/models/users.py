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

    # @model_validator(mode="after")
    # def populate_permissions(cls, values):
    #     role = values.get("role")
    #     permission_manager = await get_permission_manager()
    #     if role in await :
    #         values["permissions"] = 1
    #     else:
    #         values["permissions"] = (
    #             []
    #         )  # Default to empty list if no valid role provided
    #     return values
