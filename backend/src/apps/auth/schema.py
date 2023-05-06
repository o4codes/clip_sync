from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field

from src.apps import users
from src.libs import fields


class UserTokenSchema(BaseModel):
    id: fields.PyObjectId = Field(alias="_id")
    email: EmailStr
    device_id: fields.PyObjectId
    exp: Optional[datetime]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UserLoginRequestSchema(BaseModel):
    email: EmailStr
    password: str


class UserLoginResponseSchema(users.BasicUserResponseSchema):
    token: str
