from fastapi.encoders import jsonable_encoder

from src.libs import BaseService
from . import models, schema, repository


class DeviceService(BaseService):
    repository_klass = repository.DeviceRepository
    data_create_klass = schema.DeviceCreateSchema
    data_transfer_klass = schema.DeviceDTOSchema
    data_response_klass = models.DeviceModel
    model_klass = models.DeviceModel
    unique_fields = ["operating_system", "browser", "device_family"]

    async def get_create(self, request_instance: schema.DeviceCreateSchema):
        devices: list[models.DeviceModel] = await self.repository.search(
            many=True, **jsonable_encoder(request_instance, exclude_none=True)
        )
        if devices:
            return devices[0]
        return await self.create(request_instance=request_instance)


class UserService(BaseService):
    repository_klass = repository.UserRepository
    data_create_klass = schema.UserCreateSchema
    data_transfer_klass = schema.UserDTOSchema
    data_response_klass = schema.BasicUserResponseSchema
    model_klass = models.UserModel
    unique_fields = ["email"]

    async def create(
        self, request_instance: schema.UserCreateSchema, **kwargs
    ) -> schema.BasicUserResponseSchema:
        device_info: dict = kwargs["device_info"]
        new_user = await super().create(request_instance)
        device_info["user_id"] = new_user.id
        await DeviceService(self.database).create(
            schema.DeviceCreateSchema(**device_info)
        )
        return new_user
