from typing import Optional
from fastapi import status, Query, Depends, Body
from fastapi.routing import APIRouter

from src.libs import PyObjectId, ResponseStatus, exceptions
from src.config.dependencies import get_database, AuthDependency
from . import schema, service, models

router = APIRouter(prefix="/rooms")


router.get(
    path="",
    response_model=schema.PaginatedRoomSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AuthDependency())],
)


async def list_rooms(
    size: int = Query(default=10),
    page: int = Query(default=1),
    database_session=Depends(get_database),
):
    count, rooms = await service.RoomService(database_session).list(size, page)
    return schema.PaginatedRoomSchema(
        status=ResponseStatus.SUCCESS,
        message="List of rooms",
        data=rooms,
        total_count=count,
        page=page,
        size=size,
    )


@router.post(
    path="",
    response_model=schema.RoomResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def create_room(
    room_data: schema.RoomCreateSchema,
    database_session=Depends(get_database),
    auth=Depends(AuthDependency()),
):
    room = await service.RoomService(database_session).create(room_data, auth.device_id)
    return schema.RoomResponseSchema(
        status=ResponseStatus.SUCCESS,
        message="Room successfully created",
        data=room,
    )


@router.get(
    path="/{id_}",
    response_model=schema.RoomResponseSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AuthDependency())],
)
async def get_room(
    id_: PyObjectId,
    database_session=Depends(get_database),
):
    room = await service.RoomService(database_session).get(id_)
    return schema.RoomResponseSchema(
        status=ResponseStatus.SUCCESS,
        message="Room Succesfully Retrieved",
        data=room,
    )


@router.patch(
    path="/{id_}",
    response_model=schema.RoomResponseSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AuthDependency())],
)
async def update_room(
    id_: PyObjectId,
    room_data: schema.RoomDTOSchema,
    database_session=Depends(get_database),
):
    room = await service.RoomService(database_session).update(id_, room_data)
    return schema.RoomResponseSchema(
        status=ResponseStatus.SUCCESS,
        message="Room update success",
        data=room,
    )


@router.delete(
    path="/{id_}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_room(
    id_: PyObjectId,
    database_session=Depends(get_database),
    auth=Depends(AuthDependency()),
):
    room_service = service.RoomService(database_session)
    room = await room_service.get(id_)
    if room.created_by != auth.device_id:
        raise exceptions.ForbiddenException("Cannot delete room")
    await room_service.delete(id_)
    return None


@router.patch(
    path="/{id_}/devices/add",
    response_model=schema.RoomResponseSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AuthDependency())],
)
async def add_devices(
    id_: PyObjectId,
    devices_data: schema.DeviceRemoveAddSchema,
    database_session=Depends(get_database),
):
    room = await service.RoomService(database_session).add_devices(
        id_, devices_data.devices
    )
    return schema.RoomResponseSchema(
        status=ResponseStatus.SUCCESS,
        message="Devices add success",
        data=room,
    )


@router.patch(
    path="/{id_}/devices/remove",
    response_model=schema.RoomResponseSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AuthDependency())],
)
async def remove_devices(
    id_: PyObjectId,
    devices_data: schema.DeviceRemoveAddSchema,
    database_session=Depends(get_database),
):
    room = await service.RoomService(database_session).remove_devices(
        id_, devices_data.devices
    )
    return schema.RoomResponseSchema(
        status=ResponseStatus.SUCCESS,
        message="Devices removal success",
        data=room,
    )
