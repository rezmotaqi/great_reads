from datetime import datetime

from pydantic import BaseModel


class BookModel(BaseModel):
    name: str
    author: str
    publish_year: datetime
    number_of_pages: int
    category: str
    sub_category: str
