from datetime import datetime

from app.core.types import PydanticObjectId, Model


class BookCreateInput(Model):
    name: str
    author: str
    publish_year: datetime
    number_of_pages: int
    category: str
    sub_category: str


class BookCreateOutput(Model):
    id: PydanticObjectId
    name: str
    author: str
    publish_year: datetime
    number_of_pages: int
    category: str
    sub_category: str

