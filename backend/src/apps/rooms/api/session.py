"""
Sessions have the same concept as rooms, but sessions are not persisted.
A session is a room, for unregistered users.
A user can create or be connected one session at a time
"""

from typing import Optional, TYPE_CHECKING, Annotated
from fastapi import status, Query, Depends, Cookie
from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi.responses import StreamingResponse, JSONResponse

from .. import schema

router = APIRouter(prefix="/sessions")


@router.post(path="", response_class=JSONResponse)
async def create_session(request: Request):
    """
    Create anonymous session
    """
    ...


@router.post(path="/join", response_class=JSONResponse)
async def join_session(
    invitation_data: schema.RoomJoinInvitationSchema,
    request: Request,
):
    ...


@router.post(path="/leave", response_class=JSONResponse)
async def leave_session(request: Request):
    ...


@router.get(path="/qrcode", response_class=JSONResponse)
async def get_session_qrcode(request: Request):
    ...
