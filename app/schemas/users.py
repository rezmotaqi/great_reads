from typing import Optional

from password_strength import PasswordPolicy
from pydantic import EmailStr, Field, field_validator, SecretStr

from app.core.types import Model


class UserProfile(Model):
    first_name: str = Field(...)
    last_name: str = Field(...)
    avatar: Optional[str] = Field(...)


class UserRegistrationInput(Model):
    UserProfile: UserProfile = Field(...)
    username: EmailStr = Field(...)
    password: str = Field(...)
    repeat_password: str = Field(...)

    @field_validator('password')
    def validate_password_strength(cls, value):
        policy = PasswordPolicy()
        policy.minimum_length = 8
        policy.require_uppercase = True
        policy.require_lowercase = True
        policy.require_digits = True
        policy.require_special = True

        result = policy.test(value)
        if not result:
            raise ValueError(f"Password does not meet requirements: {result}")
        return value


class LoginInput(Model):
    username: EmailStr
    password: str
