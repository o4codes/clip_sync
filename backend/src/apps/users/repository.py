from src.libs import BaseRepository
from . import models, constants


class DeviceRepository(BaseRepository):
    model_klass = models.DeviceModel
    collection_name = constants.DEVICE_DB_COLLECTION_NAME


class UserRepository(BaseRepository):
    model_klass = models.UserModel
    collection_name = constants.USER_DB_COLLLECTION_NAME
