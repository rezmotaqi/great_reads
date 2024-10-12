from pydantic import SecretStr

from app.core.types import Model


class Permission(Model):
    pass


class Role(Model):
    name: str


class BaseRole:
    def __init__(self, role_name: str, role_description: str):
        self.role_name = role_name
        self.role_description = role_description


class LoginInput(Model):
    username: str
    password: SecretStr
