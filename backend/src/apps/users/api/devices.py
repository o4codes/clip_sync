from typing import Optional
from fastapi import status, Query, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.routing import APIRouter
from fastapi_utils.cbv import cbv

from src.libs import PyObjectId, ResponseStatus
from src.config.dependencies.database import get_database
from .. import schema, service


router = APIRouter(prefix="/devices")


@router.get(
    path="",
    response_model=schema.PaginatedDeviceSchema,
    status_code=status.HTTP_200_OK,
)
async def list_devices(
    size: int = Query(default=10),
    page: int = Query(default=1),
    database_session=Depends(get_database),
    user_id: Optional[str] = None
):
    count, devices = await service.DeviceService(database_session).list(size, page, user_id = user_id)
    return schema.PaginatedDeviceSchema(
        status=ResponseStatus.SUCCESS,
        message="List of devices",
        data=devices,
        total_count=count,
        page=page,
        size=size,
    )


@router.get(
    path="/{id_}",
    response_model=schema.DeviceResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_device(id_: PyObjectId, database_session=Depends(get_database)):
    device = await service.DeviceService(database_session).get(id_)
    return schema.DeviceResponseSchema(
        status=ResponseStatus.SUCCESS,
        message="Device successfully retrieved",
        data=device,
    )
