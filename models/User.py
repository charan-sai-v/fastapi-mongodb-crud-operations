import uuid
from typing import Optional
from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    email: str = Field(..., unique_items= None)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "Charan Sai",
                "email": "Charansai@gmail.com",
                "password": "Charan@123"
            }
        }


class UpdateUserSchema(BaseModel):
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "Charan Sai",
                "email": "Charansai@gmail.com",
                "password": "Charan@123"
            }
        }

