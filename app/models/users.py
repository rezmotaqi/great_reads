import datetime
from typing import Self

from pydantic import Field, SecretStr, field_validator, model_validator

from app.core.enums import UserStatus
from app.core.types import Model
from app.core.utils import hash_password
from app.schemas.authentication import Role, RoleFactory


class UserProfile(Model):
    avatar: str | None = None
    first_name: str
    last_name: str


class User(Model):

    profile: UserProfile | None = None
    username: str
    password: SecretStr
    status: UserStatus = Field(default=UserStatus.ACTIVE)
    permissions: list[str] = Field(
        default_factory=list,
    )
    role: Role
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow
    )
    updated_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow
    )

    @field_validator("password")
    def hash_password(cls, password: SecretStr):
        password = hash_password(password.get_secret_value())
        return password

    # noinspection PyTypeChecker
    @model_validator(mode="after")
    def populate_permissions(self, values: dict[str, str]) -> Self:
        values["permissions"] = RoleFactory.get_permission_strategy(
            values["role"]
        ).get_permissions()

        return self
