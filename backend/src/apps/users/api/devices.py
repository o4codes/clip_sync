from fastapi import status, Query, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.routing import APIRouter
from fastapi_utils.cbv import cbv

from src.libs import PyObjectId, ResponseStatus
from src.config.dependencies.database import get_database
from .. import schema, service


router = APIRouter(prefix="/devices")


@cbv(router)
class DeviceRouter:
    database_session = Depends(get_database)

    @router.get(
        path="",
        response_model=schema.PaginatedDeviceSchema,
        status_code=status.HTTP_200_OK,
    )
    async def list_devices(
        self,
        size: int = Query(default=10),
        page: int = Query(default=1),
    ):
        count, devices = await service.DeviceService(self.database_session).list(
            size, page
        )
        return schema.PaginatedDeviceSchema(
            status=ResponseStatus.SUCCESS,
            message="List of devices",
            data=devices,
            total_count=count,
            page=page,
            size=size,
        )

    @router.post(
        path="",
        response_model=schema.DeviceResponseSchema,
        status_code=status.HTTP_200_OK,
    )
    async def create_device(self, device_data: schema.DeviceCreateSchema):
        device = await service.DeviceService(self.database_session).create(device_data)
        return schema.DeviceResponseSchema(
            status=ResponseStatus.SUCCESS,
            message="Device successfully created",
            data=device,
        )

    @router.get(
        path="/{id_}",
        response_model=schema.DeviceResponseSchema,
        status_code=status.HTTP_200_OK,
    )
    async def get_device(self, id_: PyObjectId):
        device = await service.DeviceService(self.database_session).get(id_)
        return schema.DeviceResponseSchema(
            status=ResponseStatus.SUCCESS,
            message="Device successfully retrieved",
            data=device,
        )