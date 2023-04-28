from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional, Union

import orjson
import pytz
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field

from .fields import PyObjectId

if TYPE_CHECKING:
    from pydantic.typing import AbstractSetIntStr, DictStrAny, MappingIntStrAny


def orjson_dumps(v, *, default):
    """rjson.dumps returns bytes, to match standard json.dumps we need to decode
    """
    return orjson.dumps(v, default=default).decode()

class DbModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default=datetime.now().replace(tzinfo=pytz.utc))
    updated_at: Optional[datetime]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}
    
    def serializable_dict(
        self, 
        include: DictStrAny = None, 
        exclude: DictStrAny = None,
        by_alias: bool = True,
        exclude_unset: bool = False, 
        exclude_defaults: bool = False,
        exclude_none: bool = None
    ):
        """Return a dict which contains only serializable fields."""
        return jsonable_encoder(
            self, 
            include=include, 
            exclude=exclude, 
            by_alias=by_alias, 
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none
        )


class ResponseStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class DefaultResponse(BaseModel):
    status: ResponseStatus
    message: str
    data: Union[list, dict, BaseModel]


class PaginationModel(DefaultResponse):
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

