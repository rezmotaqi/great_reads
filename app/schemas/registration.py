from pydantic import Field, validator, field_validator

from app.core.types import Model


class SignupInput(Model):
    username: str
    password: str
    repeat_password: str

    @field_validator('repeat_password')
    def passwords_match(cls, repeat_password, values):
        if 'password' in values and repeat_password != values['password']:
            raise ValueError('Passwords do not match')
        return repeat_password

    @field_validator('password')
    def validate_password(cls, password):
        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(char.isdigit() for char in password):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in password):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(char.islower() for char in password):
            raise ValueError('Password must contain at least one lowercase letter')
        return password
