from typing import Optional

from pydantic import root_validator

from src.libs import DbModel, PyObjectId, exceptions


class RoomModel(DbModel):
    """
    A room is a confined space designed for devices to communicate
    The room id will be used as idempotent proeprty for the websocket rooms
    """

    name: Optional[str] = None
    devices: list[PyObjectId]
    created_by: PyObjectId  # device id of creator

    @root_validator(pre=True)
    def validate_instance(cls, values: dict):
        if values.get("created_by") not in values.get("devices"):
            raise exceptions.InternalServerException("created_by not in room")
        return values
