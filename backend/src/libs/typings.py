from typing import TypeVar

from .models import DbModel

DbModelType = TypeVar("DbModelType", bound=DbModel)
