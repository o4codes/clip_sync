from typing import Union
from pydantic import BaseModel, EmailStr, validator

from src.libs import DefaultResponse, DbModel, PaginationModel
from .models import DeviceModel, UserModel
from . import validators


class DeviceCreateSchema(BaseModel):
    username: str


class DeviceResponseSchema(DefaultResponse):
    data: UserModel


class PaginatedDeviceSchema(PaginationModel):
    data: list[UserModel]


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str

    @validator("password")
    def validate_password(cls, value: str):
        validators.password_validator(value)
        return value


class BasicUserResponseSchema(DbModel):
    email: EmailStr


class UserResponseSchema(DefaultResponse):
    data: BasicUserResponseSchema


class PaginatedUserSchema(PaginationModel):
    data: list[BasicUserResponseSchema]
