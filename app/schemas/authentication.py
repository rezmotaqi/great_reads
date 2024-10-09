from typing import List

from pydantic import BaseModel, Field
from app.core.types import Model


# class Permission(Model):


# class Role(Model):
#     name: str
#     permissions: List[Permission]


class BaseRole:
    def __init__(self, role_name: str, role_description: str):
        self.role_name = role_name
        self.role_description = role_description
