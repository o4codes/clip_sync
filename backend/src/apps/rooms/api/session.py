"""
Sessions have the same concept as rooms, but sessions are not persisted.
A session is a room, for unregistered users.
A user can create or be connected one session at a time
"""
import json
from datetime import datetime
from typing import Optional, TYPE_CHECKING, Annotated, TypedDict

from bson import ObjectId
from fastapi import status, Query, Depends, Cookie
from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel

from src.config.dependencies import Cache
from src.libs import exceptions, utils
from .. import schema, constants
from ..libs import QRCodeGenerator

router = APIRouter(prefix="/sessions")
ROOM_SESSION_KEY = "room_session"
USER_ID_KEY = "user_id"


class RoomSessionDict(TypedDict):
    room_id: str
    invite_code: str
    created_by: str


async def _get_client_session(room_session: str = None):
    if room_session:
        room_session_data: dict = json.loads(room_session)
        session_data = await Cache.get(room_session_data.get("invite_code"))
        return session_data


@router.post(path="", response_class=JSONResponse)
async def create_session(request: Request):
    """
    Create anonymous session
    """
    room_session: str = request.cookies.get(ROOM_SESSION_KEY)
    client_session = await _get_client_session(room_session)
    if client_session:
        raise exceptions.ForbiddenException("User already present in a session")
    room_id, user_id = str(ObjectId()), str(ObjectId())
    invite_code = f"{constants.ROOM_INVITE_PREFIX}-{utils.get_random_string(length=6)}"
    session_data = RoomSessionDict(
        room_id=room_id, invite_code=invite_code, created_by=user_id
    )
    response = JSONResponse(content={"status": "SUCCESS", "data": session_data})
    response.set_cookie(
        key=ROOM_SESSION_KEY,
        value=json.dumps(session_data),
        expires=datetime.now() + Cache.EXPIRY_DURATION,
    )
    response.set_cookie(
        key=USER_ID_KEY, value=user_id, expires=datetime.now() + Cache.EXPIRY_DURATION
    )
    await Cache.set(session_data, session_data.get("invite_code"))
    return response


@router.post(path="/join", response_class=JSONResponse)
async def join_session(
    invitation_data: schema.RoomJoinInvitationSchema,
    request: Request,
):
    room_session: Optional[str] = request.cookies.get(ROOM_SESSION_KEY)
    session_data = await _get_client_session(room_session)
    if session_data:
        raise exceptions.ForbiddenException("User is present in a session")
    user_id = str(ObjectId())
    session_data = await Cache.get(invitation_data.invitation_code)
    response = JSONResponse(content={"status": "SUCCESS", "data": session_data})
    response.set_cookie(
        key=ROOM_SESSION_KEY,
        value=json.dumps(session_data),
        expires=datetime.now() + Cache.EXPIRY_DURATION,
    )
    response.set_cookie(
        key=USER_ID_KEY, value=user_id, expires=datetime.now() + Cache.EXPIRY_DURATION
    )
    await Cache.set(session_data, session_data.get("invite_code"))
    return response


@router.post(path="/leave", response_class=JSONResponse)
async def leave_session(request: Request):
    room_session: Optional[str] = request.cookies.get(ROOM_SESSION_KEY)
    session_data: RoomSessionDict = await _get_client_session(room_session)
    if not session_data:
        raise exceptions.BadRequest("User is not in a session")
    user_id = request.cookies.get(USER_ID_KEY)
    await Cache.rmeove(session_data.get("invite_code"))
    response = JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    response.delete_cookie(ROOM_SESSION_KEY)
    response.delete_cookie(USER_ID_KEY)
    return response


@router.get(path="/qrcode", response_class=JSONResponse)
async def get_session_qrcode(request: Request):
    room_session: Optional[str] = request.cookies.get(ROOM_SESSION_KEY)
    session_data: RoomSessionDict = await _get_client_session(room_session)
    if not session_data:
        raise exceptions.BadRequest("User is not in a session")
    user_id = request.cookies.get(USER_ID_KEY)
    if session_data.get("created_by") != user_id:
        raise exceptions.ForbiddenException("Inadequate permission to get QR code")
    qr_bytes = QRCodeGenerator(encode_data=session_data.get("invite_code"))
    return StreamingResponse(qr_bytes, media_type="image/png")
