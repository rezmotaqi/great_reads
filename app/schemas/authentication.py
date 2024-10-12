from pydantic import SecretStr

from app.core.types import Model


class Permission(Model):
    pass


class Role:
    def __init__(self, permissions=None):
        self.permissions = permissions or []

    def has_permission(self, permission):
        return permission in self.permissions


class AdminRole(Role):
    def __init__(self):
        super().__init__(
            permissions=[
                "read_users",
                "create_users",
                "update_books",
                "delete_books",
            ]
        )


class ReaderRole(Role):
    def __init__(self):
        super().__init__(permissions=["read_books"])


class LoginInput(Model):
    username: str
    password: SecretStr
