from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from src.libs import DefaultResponse, PaginationModel, PyObjectId
from .models import RoomModel


class RoomDTOSchema(BaseModel):
    name: Optional[str] = None
    devices: list[PyObjectId] = Field(default_factory=list)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}


class RoomCreateSchema(RoomDTOSchema):
    devices: list[PyObjectId]


class RoomResponseSchema(DefaultResponse):
    data: RoomModel


class PaginatedRoomSchema(PaginationModel):
    data: list[RoomModel]


class DeviceRemoveAddSchema(BaseModel):
    devices: list[PyObjectId] = Field(default_factory=list)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class RoomJoinInvitationSchema(BaseModel):
    invitation_code: str
