from abc import ABC, abstractmethod
from enum import Enum
from typing import List

from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema


class RoleTypes(str, Enum):
    admin = "admin"
    normal_user = "normal_user"


class Role:

    def __init__(self, permissions=None):
        self.permissions = permissions or []

    def has_permission(self, permission):
        return permission in self.permissions

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
    def validate(cls, v) -> str:
        try:
            return str(v)
        except Exception:
            raise ValueError(f"Cannot validate {v}")

    @classmethod
    def __get_validators__(cls):
        yield cls.validate


class PermissionStrategy(ABC):
    @abstractmethod
    def get_permissions(self) -> list[str]:
        pass


class AdminPermissionStrategy(PermissionStrategy):
    def get_permissions(self) -> list[str]:
        return [
            "read_users",
            "create_users",
            "update_books",
            "delete_books",
        ]


class NormalUserPermissionStrategy(PermissionStrategy):
    def get_permissions(self) -> list[str]:
        return ["read_books"]


class RoleFactory:
    @staticmethod
    def get_permission_strategy(role_type: str) -> PermissionStrategy:
        if role_type == RoleTypes.admin.value:
            return AdminPermissionStrategy()
        elif role_type == RoleTypes.normal_user.value:
            return NormalUserPermissionStrategy()
        else:
            raise ValueError(f"Unknown role type: {role_type}")
