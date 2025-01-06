from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.vehicle_category.vehicle_category_dto import (
    VehicleCategoryCDTO, VehicleCategoryRDTO)
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.database import get_db
from app.shared.path_constants import AppPathConstants
from app.use_cases.vehicle_category.all_vehicle_category_case import \
    AllVehicleCategoryCase
from app.use_cases.vehicle_category.create_vehicle_category_case import \
    CreateVehicleCategoryCase
from app.use_cases.vehicle_category.delete_vehicle_category_case import \
    DeleteVehicleCategoryCase
from app.use_cases.vehicle_category.get_vehicle_category_by_id_case import \
    GetVehicleCategoryByIdCase
from app.use_cases.vehicle_category.get_vehicle_category_by_value_case import \
    GetVehicleCategoryByValueCase
from app.use_cases.vehicle_category.update_vehicle_category_case import \
    UpdateVehicleCategoryCase


class VehicleCategoryApi:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            f"{AppPathConstants.IndexPathName}",
            response_model=list[VehicleCategoryRDTO],
            summary="Список категорий ТС",
            description="Получение списка категорий ТС",
        )(self.get_all)
        self.router.post(
            f"{AppPathConstants.CreatePathName}",
            response_model=VehicleCategoryRDTO,
            summary="Создать категорию ТС",
            description="Создание категорий ТС",
        )(self.create)
        self.router.put(
            f"{AppPathConstants.UpdatePathName}",
            response_model=VehicleCategoryRDTO,
            summary="Обновить категорию ТС по уникальному ID",
            description="Обновление категорий ТС по уникальному идентификатору",
        )(self.update)
        self.router.delete(
            f"{AppPathConstants.DeleteByIdPathName}",
            response_model=bool,
            summary="Удалите категорию ТС по уникальному ID",
            description="Удаление категорий ТС по уникальному идентификатору",
        )(self.delete)
        self.router.get(
            f"{AppPathConstants.GetByIdPathName}",
            response_model=VehicleCategoryRDTO,
            summary="Получить категорию ТС по уникальному ID",
            description="Получение категорий ТС по уникальному идентификатору",
        )(self.get)
        self.router.get(
            f"{AppPathConstants.GetByValuePathName}",
            response_model=VehicleCategoryRDTO,
            summary="Получить категорию ТС по уникальному значению",
            description="Получение категорий ТС по уникальному значению",
        )(self.get_by_value)

    async def get_all(self, db: AsyncSession = Depends(get_db)):
        use_case = AllVehicleCategoryCase(db)
        try:
            return await use_case.execute()
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении всех категорий ТС",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def get(
        self, id: AppPathConstants.IDPath, db: AsyncSession = Depends(get_db)
    ):
        use_case = GetVehicleCategoryByIdCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении категорий ТС по значению",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def create(
        self, dto: VehicleCategoryCDTO, db: AsyncSession = Depends(get_db)
    ):
        use_case = CreateVehicleCategoryCase(db)
        try:
            return await use_case.execute(dto=dto)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании категории ТС",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def update(
        self,
        id: AppPathConstants.IDPath,
        dto: VehicleCategoryCDTO,
        db: AsyncSession = Depends(get_db),
    ):
        use_case = UpdateVehicleCategoryCase(db)
        try:
            return await use_case.execute(id=id, dto=dto)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании категорий ТС",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def delete(
        self, id: AppPathConstants.IDPath, db: AsyncSession = Depends(get_db)
    ):
        use_case = DeleteVehicleCategoryCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании категории ТС",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def get_by_value(
        self, value: AppPathConstants.ValuePath, db: AsyncSession = Depends(get_db)
    ):
        use_case = GetVehicleCategoryByValueCase(db)
        try:
            return await use_case.execute(value=value)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении категории ТС по значению",
                extra={"value": value, "details": str(exc)},
                is_custom=True,
            )
