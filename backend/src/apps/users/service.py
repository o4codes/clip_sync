from src.libs import BaseService
from . import models, schema, repository


class DeviceService(BaseService):
    repository_klass = repository.DeviceRepository
    data_request_klass = schema.DeviceCreateSchema
    data_response_klass = models.DeviceModel
    model_klass = models.DeviceModel
    unique_fields = ["username"]


class UserService(BaseService):
    repository_klass = repository.UserRepository
    data_request_klass = schema.UserCreateSchema
    data_response_klass = schema.BasicUserResponseSchema
    model_klass = models.UserModel
    unique_fields = ["email"]
