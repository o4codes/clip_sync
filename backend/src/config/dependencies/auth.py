from typing import TYPE_CHECKING, List, Union, TypeVar, Tuple

from bson import ObjectId
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from src.config.settings import Settings
from src.libs import exceptions, utils

from .database import get_database

security_mechanism = HTTPBearer()
app_settings = Settings()


class AuthDependency:
    """
    Authenticate a user account and attach associated device
    """

    def __init__(self, raise_exception: bool = True):
        self.raise_exception = raise_exception

    async def __call__(
        self,
        auth: HTTPAuthorizationCredentials = Depends(security_mechanism),
        database=Depends(get_database),
    ):
        from src.apps import users, auth as auth_module

        try:
            token = auth.credentials
            payload = utils.decode_access_token(token)
            await users.UserService(database).get(ObjectId(payload.get("_id")))
            await users.DeviceService(database).get(
                ObjectId([payload.get("device_id")])
            )
            return auth_module.UserTokenSchema(**payload)
        except (JWTError, exceptions.NotFoundException):
            if self.raise_exception:
                raise exceptions.UnauthorizedException("Invalid Token")
            return
