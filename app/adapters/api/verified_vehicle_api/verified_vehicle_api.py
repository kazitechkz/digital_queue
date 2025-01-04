from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import \
    PaginationVerifiedVehicleWithRelationsDTO
from app.adapters.dto.verified_vehicle.verified_vehicle_dto import (
    VerifiedVehicleCDTO, VerifiedVehicleWithRelationsDTO)
from app.adapters.filters.verified_vehicle.verified_vehicle_filter import \
    VerifiedVehicleFilter
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.database import get_db
from app.shared.path_constants import AppPathConstants
from app.use_cases.verified_vehicle.create_verified_vehicle_case import \
    CreateVerifiedVehicleCase
from app.use_cases.verified_vehicle.delete_verified_vehicle_case import \
    DeleteVerifiedVehicleCase
from app.use_cases.verified_vehicle.get_verified_vehicle_by_id_case import \
    GetVerifiedVehicleByIdCase
from app.use_cases.verified_vehicle.get_verified_vehicle_by_value_case import \
    GetVerifiedVehicleByValueCase
from app.use_cases.verified_vehicle.paginate_verified_vehicle_case import \
    PaginateVerifiedVehicleCase
from app.use_cases.verified_vehicle.update_verified_vehicle_case import \
    UpdateVerifiedVehicleCase


class VerifiedVehicleApi:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            "/",
            response_model=PaginationVerifiedVehicleWithRelationsDTO,
            summary="Список верифицированных ТС",
            description="Получение списка верифицированных ТС",
        )(self.get_all)
        self.router.post(
            "/create",
            response_model=VerifiedVehicleWithRelationsDTO,
            summary="Создать цвет ТС",
            description="Создание верифицированного ТС",
        )(self.create)
        self.router.put(
            "/update/{id}",
            response_model=VerifiedVehicleWithRelationsDTO,
            summary="Обновить цвет ТС по уникальному ID",
            description="Обновление верифицированного ТС по уникальному идентификатору",
        )(self.update)
        self.router.delete(
            "/delete/{id}",
            response_model=bool,
            summary="Удалите цвет ТС по уникальному ID",
            description="Удаление верифицированного ТС по уникальному идентификатору",
        )(self.delete)
        self.router.get(
            "/get/{id}",
            response_model=VerifiedVehicleWithRelationsDTO,
            summary="Получить цвет ТС по уникальному ID",
            description="Получение верифицированного ТС по уникальному идентификатору",
        )(self.get)
        self.router.get(
            "/get-by-value/{value}",
            response_model=VerifiedVehicleWithRelationsDTO,
            summary="Получить цвет ТС по уникальному значению",
            description="Получение верифицированного ТС по уникальному значению номера машины, описанию или отказу",
        )(self.get_by_value)

    async def get_all(
        self,
        parameters: VerifiedVehicleFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ):
        use_case = PaginateVerifiedVehicleCase(db)
        try:
            return await use_case.execute(filter=parameters)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении всех верифицированных ТС",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def get(
        self, id: AppPathConstants.IDPath, db: AsyncSession = Depends(get_db)
    ):
        use_case = GetVerifiedVehicleByIdCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении верифицированного ТС по значению",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def create(
        self, dto: VerifiedVehicleCDTO, db: AsyncSession = Depends(get_db)
    ):
        use_case = CreateVerifiedVehicleCase(db)
        try:
            return await use_case.execute(dto=dto)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании верифицированного ТС",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def update(
        self,
        id: AppPathConstants.IDPath,
        dto: VerifiedVehicleCDTO,
        db: AsyncSession = Depends(get_db),
    ):
        use_case = UpdateVerifiedVehicleCase(db)
        try:
            return await use_case.execute(id=id, dto=dto)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании верифицированного ТС",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def delete(
        self, id: AppPathConstants.IDPath, db: AsyncSession = Depends(get_db)
    ):
        use_case = DeleteVerifiedVehicleCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании верифицированного ТС",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def get_by_value(
        self, value: AppPathConstants.ValuePath, db: AsyncSession = Depends(get_db)
    ):
        use_case = GetVerifiedVehicleByValueCase(db)
        try:
            return await use_case.execute(value=value)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении верифицированного ТС по значению",
                extra={"value": value, "details": str(exc)},
                is_custom=True,
            )
