from typing import Optional, TYPE_CHECKING, Annotated
from fastapi import status, Query, Depends
from fastapi.routing import APIRouter
from fastapi.responses import StreamingResponse

from src.libs import PyObjectId, ResponseStatus, exceptions
from src.config.dependencies import get_database, AuthDependency
from .. import schema, service, models
from ..libs import QRCodeGenerator

if TYPE_CHECKING:
    from src.apps.auth.schema import UserTokenSchema

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
    db_session=Depends(get_database),
):
    count, rooms = await service.RoomService(db_session).list(size, page)
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
    db_session=Depends(get_database),
    auth=Annotated["UserTokenSchema", Depends(AuthDependency())],
):
    room = await service.RoomService(db_session).create(room_data, auth.device_id)
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
    db_session=Depends(get_database),
):
    room = await service.RoomService(db_session).get(id_)
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
    db_session=Depends(get_database),
):
    room = await service.RoomService(db_session).update(id_, room_data)
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
    db_session=Depends(get_database),
    auth=Annotated["UserTokenSchema", Depends(AuthDependency())],
):
    room_service = service.RoomService(db_session)
    room = await room_service.get(id_)
    if room.created_by != auth.device_id:
        raise exceptions.ForbiddenException("Cannot delete room")
    await room_service.delete(id_)
    return None


@router.get(
    path="/{id_}/qrcode",
    status_code=status.HTTP_200_OK,
    response_class=StreamingResponse,
)
async def get_room_qrcode(
    id_: PyObjectId,
    db_session=Depends(get_database),
    auth=Annotated["UserTokenSchema", Depends(AuthDependency())],
):
    room_service = service.RoomService(db_session)
    room: models.RoomModel = await room_service.get(id_)
    if room.created_by != auth.device_id:
        raise exceptions.ForbiddenException("Cannot create room qrcode")
    qr_bytes = QRCodeGenerator(encode_data=room.invitation_code).make()
    return StreamingResponse(qr_bytes, media_type="image/png")


@router.post(
    path="/join",
    response_model=schema.RoomResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def join_room(
    invitation_data: schema.RoomJoinInvitationSchema,
    db_session=Depends(get_database),
    auth=Annotated["UserTokenSchema", Depends(AuthDependency())],
):
    updated_room = await service.RoomService(db_session).join_room(
        invitation_data.invitation_code, auth.device_id
    )
    return schema.RoomResponseSchema(
        status=ResponseStatus.SUCCESS,
        message="Room Join success",
        data=updated_room,
    )


@router.post(
    path="{id_}/leave",
    response_model=schema.RoomResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def leave_room(
    id_: PyObjectId,
    db_session=Depends(get_database),
    auth=Annotated[Optional["UserTokenSchema"], Depends(AuthDependency())],
):
    room_service = service.RoomService(db_session)
    updated_room = await room_service.leave_room(id_, auth.device_id)
    return schema.RoomResponseSchema(
        status=ResponseStatus.SUCCESS,
        message="Room Leave Success",
        data=updated_room,
    )


@router.patch(
    path="/{id_}/devices/add",
    response_model=schema.RoomResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def add_devices(
    id_: PyObjectId,
    devices_data: schema.DeviceRemoveAddSchema,
    db_session=Depends(get_database),
    auth=Annotated["UserTokenSchema", Depends(AuthDependency())],
):
    updated_room = await service.RoomService(db_session).add_devices(
        id_, devices_data.devices, user_device=auth.device_id
    )
    return schema.RoomResponseSchema(
        status=ResponseStatus.SUCCESS,
        message="Devices add success",
        data=updated_room,
    )


@router.patch(
    path="/{id_}/devices/remove",
    response_model=schema.RoomResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def remove_devices(
    id_: PyObjectId,
    devices_data: schema.DeviceRemoveAddSchema,
    db_session=Depends(get_database),
    auth=Annotated["UserTokenSchema", Depends(AuthDependency())],
):
    updated_room = await service.RoomService(db_session).remove_devices(
        id_, devices_data.devices, user_device=auth.device_id
    )
    return schema.RoomResponseSchema(
        status=ResponseStatus.SUCCESS,
        message="Devices removal success",
        data=updated_room,
    )
