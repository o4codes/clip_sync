from fastapi.encoders import jsonable_encoder
from pymongo.collection import Collection
from pydantic import EmailStr

from src.libs import exceptions, utils
from src.apps import users
from . import schema


class AuthService:
    """
    Auth service performs the flow of authenticating a registered user to platform.
    Therefore, the following functions will be necessary: login, forgot-password, change-password
    """

    def __init__(self, database):
        self.database = database
        self.users_collection: Collection = database[self.USERS_COLLECTION_NAME]

    async def login(
        self, email: EmailStr, password: str, device_info: users.DeviceCreateSchema
    ) -> schema.UserLoginResponseSchema:
        """Logs a user in by generating token

        Args:
            email (EmailStr): email address of user
            password (str): password of user

        Raises:
            exceptions.BadRequest: When Email Address is not found
            exceptions.BadRequest: When Password is invalid
            exceptions.ForbiddenException: When a user is not active

        Returns:
            schema.UserLoginResponseSchema: success response of user on login
        """
        user_db = await self.users_collection.find_one({"email": email})
        if not user_db:
            raise exceptions.BadRequest("User with email address not found")
        user = users.UserModel(**user_db)
        if not utils.verify_hash(user.password, password):
            raise exceptions.BadRequest("Invalid Password")
        user_data = jsonable_encoder(user)
        device = await users.DeviceService(self.database).get_create(device_info)
        token_schema = schema.UserTokenSchema(**user_data, device_id=device.id)
        token = utils.create_access_token(data=jsonable_encoder(token_schema))
        return schema.UserLoginResponseSchema(**user_data, token=token)
