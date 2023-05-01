from typing import Optional, Any

from pydantic import EmailStr, BaseModel

from src.libs import DbModel, PyObjectId


class DeviceModel(DbModel):
    """
    A device may either have or not have a user.
    Such cases means that the device owner doesn't have an account.
    """

    operating_system: Optional[str] = None
    browser: Optional[str] = None
    device_family: Optional[str] = None
    device_model: Optional[str] = None
    device_brand: Optional[str] = None
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
