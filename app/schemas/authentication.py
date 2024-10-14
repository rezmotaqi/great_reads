from typing import Any

from pydantic import SecretStr
from pydantic_core import core_schema

from app.core.types import Model


class Role:

    def __init__(self, permissions=None):
        self.permissions = permissions or []

    def __get_pydantic_core_schema__(
        self, handler: Any
    ) -> core_schema.CoreSchema:
        # Return a simple schema without further recursion
        return core_schema.general_plain_schema(type(self))

    def has_permission(self, permission):
        return permission in self.permissions

    def generate_permissions(self):
        return self.permissions


# Custom Pydantic field type for Role
# class PydanticRole:
#     @classmethod
#     def validate(cls, value: Any) -> Role:
#         if isinstance(value, Role):
#             return value
#         elif isinstance(value, str):
#             if value == "AdminUser":
#                 return AdminUser()
#             elif value == "NormalUser":
#                 return NormalUser()
#             else:
#                 raise ValueError("Invalid role type")
#         raise TypeError("Value must be a Role instance or valid role string")
#
#     @classmethod
#     def __get_pydantic_core_schema__(cls, source_type, handler):
#         return core_schema.general_plain_schema(source_type)


class AdminUser(Role):
    def __init__(self):
        super().__init__(
            permissions=[
                "read_users",
                "create_users",
                "update_books",
                "delete_books",
            ]
        )


class NormalUser(Role):
    def __init__(self):
        super().__init__(permissions=["read_books"])


class LoginInput(Model):
    username: str
    password: SecretStr
