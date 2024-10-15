from typing import Any

from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema


class Role:

    def __init__(self, permissions=None):
        self.permissions = permissions or []

    def has_permission(self, permission):
        return permission in self.permissions

    def generate_permissions(self):
        return self.permissions

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def validate(cls, data: Any):
        if not isinstance(data, str):
            raise ValueError("Role must be a string.")
        # Custom validation logic
        permissions = data.split(",")  # Assume permissions are comma-separated
        return cls(permissions=permissions)  # Return an instance of Role


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
