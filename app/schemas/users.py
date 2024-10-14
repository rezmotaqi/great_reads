from typing import Optional

from pydantic import (
    EmailStr,
    Field,
    SecretStr,
    model_validator,
)
from typing_extensions import Self

from app.core.types import Model, PydanticObjectId
from app.schemas.authentication import Role


class UserProfile(Model):
    first_name: str = Field(...)
    last_name: str = Field(...)
    avatar: Optional[str] = Field(...)


class UserRegistrationInput(Model):
    profile: UserProfile = Field(...)
    username: EmailStr = Field(...)
    password: str = Field(...)
    repeat_password: str = Field(...)

    # @field_validator("password")
    # def validate_password_strength(cls, value):
    #     policy = PasswordPolicy()
    #     policy.minimum_length = 8
    #     policy.require_uppercase = True
    #     policy.require_lowercase = True
    #     policy.require_digits = True
    #     policy.require_special = True
    #
    #     result = policy.test(value)
    #     if not result:
    #         raise ValueError(
    #         f"Password does not meet requirements: {result}"
    #         )
    #     return value


class CompleteUserDatabaseOutput(Model):
    profile: UserProfile = Field(...)
    username: EmailStr = Field(...)
    permissions: list = Field(...)


class CurrentUser(Model):
    user_id: PydanticObjectId = Field(
        description="User id", validation_alias="_id"
    )
    profile: UserProfile = Field(...)
    username: EmailStr = Field(...)
    permissions: list = Field(...)


class CreateUserInput(Model):
    profile: UserProfile = Field(...)
    username: EmailStr = Field(...)
    permissions: Optional[list] = Field(...)
    role: Optional[Role]
    password: SecretStr = Field(...)
    repeat_password: SecretStr = Field(...)

    # @model_validator(mode="after")
    # def check_passwords_match(self) -> Self:
    #     pw1 = self.password1
    #     pw2 = self.repeat_password
    #     if pw1 is not None and pw2 is not None and pw1 != pw2:
    #         raise ValueError("passwords do not match")
    #     return self

    # @model_validator(mode="after")
    # def check_role_permissions(self) -> Self:
    #     if self.role is None or self.permissions is None:
    #         raise ValueError("role or permissions is not set")


class CreateUserOutput(Model):
    profile: UserProfile = Field(...)
    username: EmailStr = Field(...)
    permissions: list = Field(...)
