from datetime import datetime
from typing import Union, Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr, validator


from src.libs import DefaultResponse, DbModel, PaginationModel, utils, PyObjectId
from .models import DeviceModel
from . import validators


class DeviceCreateSchema(BaseModel):
    operating_system: Optional[str] = None
    browser: Optional[str] = None
    device_family: Optional[str] = None
    device_model: Optional[str] = None
    device_brand: Optional[str] = None
    user_id: Optional[PyObjectId] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}


class DeviceResponseSchema(DefaultResponse):
    data: DeviceModel


class PaginatedDeviceSchema(PaginationModel):
    data: list[DeviceModel]


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str

    @validator("password")
    def validate_password(cls, value: str):
        validators.password_validator(value)
        return utils.get_string_hash(value)


class BasicUserResponseSchema(DbModel):
    email: EmailStr


class UserResponseSchema(DefaultResponse):
    data: BasicUserResponseSchema


class PaginatedUserSchema(PaginationModel):
    data: list[BasicUserResponseSchema]
