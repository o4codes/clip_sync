from src.libs import BaseRepository
from . import models, constants


class RoomRepository(BaseRepository):
    model_klass = models.RoomModel
    collection_name = constants.ROOM_DB_COLLECTION_NAME
