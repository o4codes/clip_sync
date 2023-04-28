import re
import string
from typing import NoReturn

from src.libs import exceptions

from . import constants


def password_validator(value: str) -> NoReturn:
    # validate alphanumeric and contains special character
    pattern = r"^(?=.*[0-9a-zA-Z])(?=.*[^0-9a-zA-Z])"
    if not bool(re.match(pattern, value)):
        raise exceptions.BadRequest(
            "password must be alphanumeric and contain special characters"
        )
    # validate character length
    if len(value) <= constants.MIN_PASSWORD_LENGTH:
        raise exceptions.BadRequest("password length must be greater than 6 characters")
    # validate special character prescence
    if not bool(set(value).intersection(set(string.punctuation))):
        raise exceptions.BadRequest(
            "password must contain at least one special character"
        )
