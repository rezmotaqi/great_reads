
from bson import ObjectId
from pydantic import BaseModel


class PydanticObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError(f"Invalid BaseObjectId: {v}")
        if isinstance(v, ObjectId):
            return v
        return ObjectId(v)


class Model(BaseModel):
    class Config:
        datetime_format = "%Y-%m-%d %H:%M:%S"
        json_encoders = {
            PydanticObjectId: lambda v: str(v)  # You can define how to encode PydanticObjectId
            # datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")

        }
