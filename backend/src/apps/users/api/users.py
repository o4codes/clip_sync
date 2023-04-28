from fastapi import status, Query, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.routing import APIRouter
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from src.libs import PyObjectId, ResponseStatus
from src.config.dependencies.database import get_database
from .. import schema, service


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
    user_data: schema.UserCreateSchema, database_session=Depends(get_database)
):
    user = await service.UserService(database_session).create(user_data)
    return schema.UserResponseSchema(
        status=ResponseStatus.SUCCESS,
        message="User account successfully create",
        data=user,
    )


@router.get(
    path="/{id_}",
    response_model=schema.UserResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_user(id_: PyObjectId, database_session=Depends(get_database)):
    user = await service.UserService(database_session).get(id_)
    return schema.UserResponseSchema(
        status=ResponseStatus.SUCCESS,
        message="User acount successfully retrieved",
        data=user,
    )
