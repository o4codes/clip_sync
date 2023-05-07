from typing import Optional
from fastapi import status, Query, Depends, Header
from fastapi.routing import APIRouter

from src.libs import PyObjectId, ResponseStatus, utils
from src.config.dependencies import get_database, AuthDependency
from .. import schema, service, models


router = APIRouter(prefix="/users")


@router.get(
    path="",
    response_model=schema.PaginatedUserSchema,
    status_code=status.HTTP_200_OK,
)
async def list_users(
    size: int = Query(default=10),
    page: int = Query(default=1),
    database_session=Depends(get_database),
):
    count, users = await service.UserService(database_session).list(size, page)
    return schema.PaginatedUserSchema(
        status=ResponseStatus.SUCCESS,
        message="List of Users",
        data=users,
        total_count=count,
        page=page,
        size=size,
    )


@router.post(
    path="",
    response_model=schema.UserResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def create_user(
    user_data: schema.UserCreateSchema,
    database_session=Depends(get_database),
    user_agent: Optional[str] = Header(default=None),
):
    device_info = utils.parse_user_agent(user_agent)
    user = await service.UserService(database_session).create(user_data, device_info)
    return schema.UserResponseSchema(
        status=ResponseStatus.SUCCESS,
        message="User account successfully create",
        data=user,
    )


@router.get(
    path="/{id_}",
    response_model=schema.UserResponseSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AuthDependency())],
)
async def get_user(
    id_: PyObjectId,
    database_session=Depends(get_database),
):
    user = await service.UserService(database_session).get(id_)
    return schema.UserResponseSchema(
        status=ResponseStatus.SUCCESS,
        message="User acount successfully retrieved",
        data=user,
    )
