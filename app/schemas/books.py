from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel

from app.core.types import PydanticObjectId


class BookCreateInput(BaseModel):
    name: str
    author: str
    publish_year: datetime
    number_of_pages: int
    category: str
    sub_category: str


class BookCreateOutput(BaseModel):
    id: PydanticObjectId
    name: str
    author: str
    publish_year: datetime
    number_of_pages: int
    category: str
    sub_category: str

