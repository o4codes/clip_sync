from typing import Optional

from fastapi import Depends, Header
from fastapi.routing import APIRouter

from src.config.dependencies.database import get_database

from . import schema, service

router = APIRouter(prefix="/auth")


@router.post(path="/login", response_model=schema.UserLoginResponseSchema)
async def login_user(
    user_login_request: schema.UserLoginRequestSchema,
    user_agent: Optional[str] = Header(default=None),
    database=Depends(get_database),
):
    auth_service = service.AuthService(database)
    login_response = await auth_service.login(
        email=user_login_request.email, password=user_login_request.password
    )
    return login_response
