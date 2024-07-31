from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional

class User(BaseModel):
    id: Optional[ObjectId] = Field(alias="_id")
    username: str
    hashed_password: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}