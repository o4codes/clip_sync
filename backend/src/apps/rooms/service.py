from typing import List, Union

from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from src.apps import users
from src.libs import BaseService, exceptions
from . import models, schema, repository


class RoomService(BaseService):
    repository_klass = repository.RoomRepository
    data_request_klass = schema.RoomCreateSchema
    data_response_klass = models.RoomModel
    model_klass = models.RoomModel
    unique_fields = ["devices"]

    async def __validate_devices(self, devices: list[ObjectId]):
        search_kwargs = {"_id": {"$in": devices}}
        searched_devices = await users.DeviceRepository(self.database).search(
            many=True, **search_kwargs
        )
        searched_devices_ids = [device["_id"] for device in searched_devices]
        if not all(device_id in searched_devices_ids for device_id in devices):
            raise exceptions.BadRequest("Some Device Ids are not valid")

    async def create(
        self, request_instance: schema.RoomCreateSchema
    ) -> models.RoomModel:
        """Creates entity into database

        Args:
            request_instance[BaseModel]: pydantic object of entity data to insert into database

        Returns:
            BaseModel: pydantic object of data inserted

        Raises:
            BadRequest: When unique data already exists
        """
        db_model_instance = self.model_klass(**request_instance.dict())
        search_kwargs = {"devices": {"$all": request_instance.devices}}
        if await self.repository.search(**search_kwargs):
            raise exceptions.BadRequest(
                "Cannot create room, due to existence of room containing exact members"
            )
        self.__validate_devices(request_instance.devices)
        db_result = await self.repository.create(db_model_instance)
        response = self.data_response_klass(**db_result.dict())
        return response

    async def update(
        self, id_: ObjectId, update_instance: schema.RoomCreateSchema
    ) -> BaseModel:
        """Updates entity data in database

        Args:
            id_[ObjectId]: primary key of entity to be updated
            update_instance [BaseModel]: update data

        Returns:
            BaseModel: updated entity

        Raises:
            BadRequest: when unique data already exists in database
        """
        room: models.RoomModel = self.get(id_)
        search_kwargs = {"devices": {"$all": update_instance.devices}}
        if await self.repository.search(**search_kwargs):
            raise exceptions.BadRequest(
                "Cannot create room, due to existence of room containing exact members"
            )
        update_data = jsonable_encoder(
            update_instance, exclude_none=True, exclude_unset=True
        )
        updated_room = room.copy(update_data)
        self.__validate_devices(updated_room.devices)
        db_result = await self.repository.update(id_, updated_room)
        response = self.data_response_klass(**jsonable_encoder(db_result))
        return response

    async def add_devices(self, id_: ObjectId, devices: list[ObjectId]):
        """Adds devices to room

        Args:
            devices [list[ObjectId]]: list of devices to be added
        """
        self.__validate_devices(devices)
        room: models.RoomModel = await self.get(id_)
        room.devices.extend(devices)
        db_result = await self.repository.update(id_, room)
        response = self.data_response_klass(**jsonable_encoder(db_result))
        return response

    async def remove_devices(self, id_: ObjectId, devices: list[ObjectId]):
        """Adds devices to room

        Args:
            devices [list[ObjectId]]: list of devices to be added
        """
        self.__validate_devices(devices)
        room: models.RoomModel = await self.get(id_)
        room.devices = [device for device in room.devices if device not in devices]
        db_result = await self.repository.update(id_, room)
        response = self.data_response_klass(**jsonable_encoder(db_result))
        return response
