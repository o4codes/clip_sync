from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional, Union

import pytz
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field

from .fields import PyObjectId

if TYPE_CHECKING:
    from pydantic.typing import AbstractSetIntStr, DictStrAny, MappingIntStrAny


class DbModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default=datetime.now().replace(tzinfo=pytz.utc))
    updated_at: Optional[datetime]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}


class PaginationModel(BaseModel):
    total_count: int
    page: int
    size: int
    data: list[BaseModel]

    @property
    def total_pages(self) -> int:
        if self.total_count == 0:
            return 0
        return (self.total_count - 1) // self.size + 1

    def paginate(self) -> dict:
        return_data = jsonable_encoder(self)
        return_data["total_pages"] = self.total_pages
        return return_data

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}


class ErrorModelStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"


class ErrorModel(BaseModel):
    status: ErrorModelStatus
    message: str
    details: Union[str, list, dict]
    timestamp: float = datetime.now().timestamp()
