"""
Sessions have the same concept as rooms, but sessions are not persisted.
A session is a room, for unregistered users.
A user can create or be connected one session at a time
"""


from typing import Optional, TYPE_CHECKING, Annotated
from fastapi import status, Query, Depends
from fastapi.routing import APIRouter
from fastapi.responses import StreamingResponse


router = APIRouter(prefix="/sessions")

