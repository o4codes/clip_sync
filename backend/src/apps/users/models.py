from typing import Optional, Any

from pydantic import EmailStr

from src.libs import DbModel, PyObjectId


class DeviceModel(DbModel):
    """
    Holds information about device being used to share clips
    A device may either have or not have a user.
    Such cases means that the device owner doesn't have an account.
    """
    device_name: str
    username: str
    user_id: Optional[PyObjectId] = None


class UserModel(DbModel):
    """
    Holds information about a user.
    Users can have multiple devices all linked to one another.
    Also different groups/rooms can be created for some set of devices.
    """
    email: EmailStr
    password: str
    subscription: Any = None