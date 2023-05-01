from pydantic import BaseModel
from src.libs import BaseService
from . import models, schema, repository


class DeviceService(BaseService):
    repository_klass = repository.DeviceRepository
    data_request_klass = schema.DeviceCreateSchema
    data_response_klass = models.DeviceModel
    model_klass = models.DeviceModel
    unique_fields = ["operating_system", "device_model"]


class UserService(BaseService):
    repository_klass = repository.UserRepository
    data_request_klass = schema.UserCreateSchema
    data_response_klass = schema.BasicUserResponseSchema
    model_klass = models.UserModel
    unique_fields = ["email"]
    
    async def create(self, request_instance: schema.UserCreateSchema, **kwargs) -> schema.BasicUserResponseSchema:
        device_info: dict = kwargs['device_info']
        new_user = await super().create(request_instance)
        device_info['user_id'] = new_user.id
        await DeviceService(self.database).create(schema.DeviceCreateSchema(**device_info))
        return new_user
