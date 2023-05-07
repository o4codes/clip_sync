from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel

from src.libs import DefaultResponse, PaginationModel, PyObjectId
from .models import RoomModel


class RoomCreateSchema(BaseModel):
    name: Optional[str] = None
    devices: list[PyObjectId]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}


class RoomResponseSchema(DefaultResponse):
    data: RoomModel


class PaginatedRoomSchema(PaginationModel):
    data: list[RoomModel]
