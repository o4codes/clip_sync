from datetime import datetime
from typing import Union, Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr, validator

from src.libs import DefaultResponse, DbModel, PaginationModel, utils, PyObjectId
from .models import DeviceModel
from . import validators


class DeviceDTOSchema(BaseModel):
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


class DeviceCreateSchema(DeviceDTOSchema):
    user_id: PyObjectId


class DeviceResponseSchema(DefaultResponse):
    data: DeviceModel


class PaginatedDeviceSchema(PaginationModel):
    data: list[DeviceModel]


class UserDTOSchema(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    @validator("password")
    def validate_password(cls, value: str = None):
        if not value:
            return
        validators.password_validator(value)
        return utils.get_string_hash(value)


class UserCreateSchema(UserDTOSchema):
    email: EmailStr
    password: str


class BasicUserResponseSchema(DbModel):
    email: EmailStr


class UserResponseSchema(DefaultResponse):
    data: BasicUserResponseSchema


class PaginatedUserSchema(PaginationModel):
    data: list[BasicUserResponseSchema]
