"""
Sessions have the same concept as rooms, but sessions are not persisted.
A session is a room, for unregistered users.
A user can create or be connected one session at a time
"""
import json
from datetime import datetime, timezone
from typing import Optional, TypedDict

import pytz
from bson import ObjectId
from fastapi import File, Form, Header, UploadFile, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.routing import APIRouter
from src.config.dependencies import Cache
from src.libs import WebsocketEvents, exceptions, utils, websocket_emitter
from starlette.background import BackgroundTasks

from .. import constants, schema
from ..libs import QRCodeGenerator

router = APIRouter(prefix="/sessions")
ROOM_SESSION_KEY = "room_session"
USER_SESSION_KEY = "user_session"


class EventDataDict(TypedDict):
    event: WebsocketEvents
    data: dict


async def _get_client_session(room_session: str = None):
    if room_session:
        room_session_data: dict = json.loads(room_session)
        session_data = await Cache.get(room_session_data.get("invite_code"))
        return session_data


def generate_username(user_agent: str):
    parsed_user_agent = utils.parse_user_agent(user_agent)
    return (
        f"{parsed_user_agent.get('device_brand') or ''} {parsed_user_agent.get('os')}"
    )


def generate_background_tasks(room_id: str, events: list[EventDataDict]):
    tasks = BackgroundTasks()
    for event, data in events:
        tasks.add_task(
            websocket_emitter.publish,
            channel=room_id,
            event=event,
            data=data,
        )
    return tasks


@router.post(path="", response_class=JSONResponse)
async def create_session(
    request: Request, user_agent: Optional[str] = Header(default=None)
):
    """
    Create anonymous session
    """
    room_session: str = request.cookies.get(ROOM_SESSION_KEY)
    client_session = await _get_client_session(room_session)
    if client_session:
        raise exceptions.ForbiddenException("User already present in a session")
    room_id, user_id = str(ObjectId()), str(ObjectId())
    username = generate_username(user_agent)
    invite_code = f"{constants.ROOM_INVITE_PREFIX}-{utils.get_random_string(length=6)}"
    session_data = schema.SessionCreateSchema(
        room_id=room_id, invite_code=invite_code, user_id=user_id, username=username
    ).dict()
    user_data = schema.SessionUserSchema(username=username, user_id=user_id).dict()
    tasks = generate_background_tasks(
        session_data.get("room_id"),
        [
            {
                "event": WebsocketEvents.ROOM_CREATED,
                "data": session_data,
            }
        ],
    )
    expires_dt = datetime.now() + Cache.EXPIRY_DURATION
    response = JSONResponse(
        content={"status": "SUCCESS", "data": session_data}, background=tasks
    )
    response.set_cookie(
        key=ROOM_SESSION_KEY,
        value=json.dumps(session_data),
        expires=expires_dt.astimezone(timezone.utc),
    )
    response.set_cookie(
        key=USER_SESSION_KEY,
        value=user_data,
        expires=expires_dt.astimezone(timezone.utc),
    )
    await Cache.set(session_data, session_data.get("invite_code"))
    return response


@router.post(path="/join", response_class=JSONResponse)
async def join_session(
    invitation_data: schema.RoomJoinInvitationSchema,
    request: Request,
    user_agent: Optional[str] = Header(default=None),
):
    room_session: Optional[str] = request.cookies.get(ROOM_SESSION_KEY)
    session_data = await _get_client_session(room_session)
    if session_data:
        raise exceptions.ForbiddenException("User is present in a session")
    user_data = schema.SessionUserSchema(
        username=generate_username(user_agent), user_id=str(ObjectId())
    ).dict()
    if session_data.get("invite_code") != invitation_data.invitation_code:
        raise exceptions.BadRequest("Invalid invitation code")
    tasks = generate_background_tasks(
        room_id=session_data.get("room_id"),
        events=[
            {
                "event": WebsocketEvents.ROOM_JOINED,
                "data": schema.SessionJoinLeaveSchema(
                    room_id=session_data.get("room_id"), **user_data
                ).dict(),
            }
        ],
    )
    response = JSONResponse(
        content={"status": "SUCCESS", "data": session_data}, background=tasks
    )
    response.set_cookie(
        key=ROOM_SESSION_KEY,
        value=json.dumps(session_data),
        expires=datetime.utcnow() + Cache.EXPIRY_DURATION,
    )
    response.set_cookie(
        key=USER_SESSION_KEY,
        value=user_data,
        expires=datetime.utcnow() + Cache.EXPIRY_DURATION,
    )
    await Cache.set(session_data, session_data.get("invite_code"))
    return response


@router.post(path="/leave", response_class=JSONResponse)
async def leave_session(request: Request):
    room_session: Optional[str] = request.cookies.get(ROOM_SESSION_KEY)
    session_data = await _get_client_session(room_session)
    user_data = request.cookies.get(USER_SESSION_KEY)
    if not session_data:
        raise exceptions.BadRequest("User is not in a session")
    await Cache.remove(session_data.get("invite_code"))
    tasks = generate_background_tasks(
        room_id=session_data.get("room_id"),
        events=[
            {
                "event": WebsocketEvents.ROOM_LEFT,
                "data": schema.SessionJoinLeaveSchema(
                    room_id=session_data.get("room_id"), **user_data
                ).dict(),
            }
        ],
    )
    response = JSONResponse(status_code=status.HTTP_204_NO_CONTENT, background=tasks)
    response.delete_cookie(ROOM_SESSION_KEY)
    response.delete_cookie(USER_SESSION_KEY)
    return response


@router.get(path="/qrcode", response_class=JSONResponse)
async def get_session_qrcode(request: Request):
    room_session: Optional[str] = request.cookies.get(ROOM_SESSION_KEY)
    session_data = await _get_client_session(room_session)
    if not session_data:
        raise exceptions.BadRequest("User is not in a session")
    user_data = request.cookies.get(USER_SESSION_KEY)
    if session_data.get("user_id") != user_data.get("user_id"):
        raise exceptions.ForbiddenException("Inadequate permission to get QR code")
    qr_bytes = QRCodeGenerator(encode_data=session_data.get("invite_code")).make()
    return StreamingResponse(qr_bytes, media_type="image/png")


@router.get(path="/message", response_class=JSONResponse)
async def send_message(
    request: Request,
    text: Optional[str] = Form(default=None, description="Text Message"),
    media: Optional[UploadFile] = File(default=None, description="Media Message"),
):
    room_session: Optional[str] = request.cookies.get(ROOM_SESSION_KEY)
    session_data = await _get_client_session(room_session)
    if not session_data:
        raise exceptions.BadRequest("User is not in a session")
    if len(list(filter(lambda bool: (text, media)))) != 1:
        raise exceptions.BadRequest("Only one of text or media is required")
    return JSONResponse(content={"status": "SUCCESS", "message": "Message sent"})
