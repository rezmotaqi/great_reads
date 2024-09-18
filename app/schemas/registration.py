from pydantic import Field

from app.core.types import Model


class SignupInput(Model):
    username: str
    password: str
    repeat_password: str

