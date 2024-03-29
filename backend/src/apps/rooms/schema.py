from datetime import datetime
from typing import Optional, TypedDict

from bson import ObjectId
from pydantic import BaseModel, Field
from src.libs import DefaultResponse, PaginationModel, PyObjectId, WebsocketEvents

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


class SessionUserSchema(BaseModel):
    user_id: str
    username: str


class SessionCreateSchema(SessionUserSchema):
    room_id: str
    invite_code: str


class SessionJoinLeaveSchema(SessionUserSchema):
    room_id: str


class SessionTextMessageSchema(SessionJoinLeaveSchema):
    message: str


class EventDataDict(TypedDict):
    event: WebsocketEvents
    data: dict
