from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.vehicle_color.vehicle_color_dto import (
    VehicleColorCDTO,
    VehicleColorRDTO,
)
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.database import get_db
from app.shared.path_constants import AppPathConstants
from app.use_cases.vehicle_color.all_vehicle_color_case import AllVehicleColorCase
from app.use_cases.vehicle_color.create_vehicle_color_case import CreateVehicleColorCase
from app.use_cases.vehicle_color.delete_vehicle_color_case import DeleteVehicleColorCase
from app.use_cases.vehicle_color.get_vehicle_color_by_id_case import (
    GetVehicleColorByIdCase,
)
from app.use_cases.vehicle_color.get_vehicle_color_by_value_case import (
    GetVehicleColorByValueCase,
)
from app.use_cases.vehicle_color.update_vehicle_color_case import UpdateVehicleColorCase


class VehicleColorApi:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            "/",
            response_model=list[VehicleColorRDTO],
            summary="Список цветов ТС",
            description="Получение списка цветов ТС",
        )(self.get_all)
        self.router.post(
            "/create",
            response_model=VehicleColorRDTO,
            summary="Создать цвет ТС",
            description="Создание цвета ТС",
        )(self.create)
        self.router.put(
            "/update/{id}",
            response_model=VehicleColorRDTO,
            summary="Обновить цвет ТС по уникальному ID",
            description="Обновление цвета ТС по уникальному идентификатору",
        )(self.update)
        self.router.delete(
            "/delete/{id}",
            response_model=bool,
            summary="Удалите цвет ТС по уникальному ID",
            description="Удаление цвета ТС по уникальному идентификатору",
        )(self.delete)
        self.router.get(
            "/get/{id}",
            response_model=VehicleColorRDTO,
            summary="Получить цвет ТС по уникальному ID",
            description="Получение цвета ТС по уникальному идентификатору",
        )(self.get)
        self.router.get(
            "/get-by-value/{value}",
            response_model=VehicleColorRDTO,
            summary="Получить цвет ТС по уникальному значению",
            description="Получение цвета ТС по уникальному значению",
        )(self.get_by_value)

    async def get_all(self, db: AsyncSession = Depends(get_db)):
        use_case = AllVehicleColorCase(db)
        try:
            return await use_case.execute()
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении всех цветов",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def get(
        self, id: AppPathConstants.IDPath, db: AsyncSession = Depends(get_db)
    ):
        use_case = GetVehicleColorByIdCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении цвета ТС по значению",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def create(self, dto: VehicleColorCDTO, db: AsyncSession = Depends(get_db)):
        use_case = CreateVehicleColorCase(db)
        try:
            return await use_case.execute(dto=dto)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании цвета ТС",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def update(
        self,
        id: AppPathConstants.IDPath,
        dto: VehicleColorCDTO,
        db: AsyncSession = Depends(get_db),
    ):
        use_case = UpdateVehicleColorCase(db)
        try:
            return await use_case.execute(id=id, dto=dto)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании цвета ТС",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def delete(
        self, id: AppPathConstants.IDPath, db: AsyncSession = Depends(get_db)
    ):
        use_case = DeleteVehicleColorCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании цвета ТС",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def get_by_value(
        self, value: AppPathConstants.ValuePath, db: AsyncSession = Depends(get_db)
    ):
        use_case = GetVehicleColorByValueCase(db)
        try:
            return await use_case.execute(value=value)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении цвета ТС по значению",
                extra={"value": value, "details": str(exc)},
                is_custom=True,
            )
