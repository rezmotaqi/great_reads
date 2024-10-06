from datetime import datetime
from enum import Enum

from app.core.types import Model


class Category(str, Enum):
    Novel = "novel"


class BookCreateInput(Model):
    name: str
    author: str
    publish_year: datetime
    number_of_pages: int
    category: Category
    # sub_category:


class BookCreateOutput(Model):
    book_id: str
    author: str
    publish_year: datetime
    number_of_pages: int
    category: str
    sub_category: str
