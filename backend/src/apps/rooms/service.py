from typing import List, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from src.libs import BaseService, exceptions
from . import models, schema, repository


class RoomService(BaseService):
    repository_klass = repository.RoomRepository
    data_request_klass = schema.RoomCreateSchema
    data_response_klass = models.RoomModel
    model_klass = models.RoomModel
    unique_fields = ["devices"]
    
    async def create(self, request_instance: schema.RoomCreateSchema) -> models.RoomModel:
        """Creates entity into database

        Args:
            request_instance[BaseModel]: pydantic object of entity data to insert into database

        Returns:
            BaseModel: pydantic object of data inserted

        Raises:
            BadRequest: When unique data already exists
        """
        db_model_instance = self.model_klass(**request_instance.dict())
        search_kwargs = { "devices": { "$all" : request_instance.devices } }
        if await self.repository.search(**search_kwargs):
            raise exceptions.BadRequest(
                "Cannot create data contains already exsiting unique properties"
            )
        db_result = await self.repository.create(db_model_instance)
        response = self.data_response_klass(**db_result.dict())
        return response