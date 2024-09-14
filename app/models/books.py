from pydantic import BaseModel


class BookModel(BaseModel):
    name: str
    author: str
    publish_year: int
    number_of_pages: int
    category: str
    sub_category: str
