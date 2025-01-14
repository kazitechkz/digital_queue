from typing import List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationVehicleWithRelationsDTO
from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.adapters.dto.vehicle.vehicle_dto import VehicleCDTO, VehicleWithRelationsDTO
from app.adapters.filters.vehicle.client.vehicle_client_filter import (
    VehicleClientFilter,
)
from app.adapters.filters.vehicle.vehicle_filter import VehicleFilter
from app.core.api_middleware_core import check_client
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.database import get_db
from app.shared.app_file_constants import AppFileExtensionConstants
from app.shared.path_constants import AppPathConstants
from app.use_cases.file.save_file_case import SaveFileCase
from app.use_cases.vehicle.client.add_client_vehicle_case import AddClientVehicleCase
from app.use_cases.vehicle.client.all_client_vehicle_case import AllClientVehicleCase
from app.use_cases.vehicle.client.edit_client_vehicle_case import EditClientVehicleCase
from app.use_cases.vehicle.client.paginate_client_vehicle_case import (
    PaginateClientVehicleCase,
)
from app.use_cases.vehicle.create_vehicle_case import CreateVehicleCase
from app.use_cases.vehicle.delete_vehicle_case import DeleteVehicleCase
from app.use_cases.vehicle.get_vehicle_by_id_case import GetVehicleByIdCase
from app.use_cases.vehicle.get_vehicle_by_value_case import GetVehicleByValueCase
from app.use_cases.vehicle.paginate_vehicle_case import PaginateVehicleCase
from app.use_cases.vehicle.update_vehicle_case import UpdateVehicleCase


class VehicleApi:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            f"{AppPathConstants.IndexPathName}",
            response_model=PaginationVehicleWithRelationsDTO,
            summary="Список транспортных средств",
            description="Получение списка транспортных средств",
        )(self.get_all)
        self.router.post(
            f"{AppPathConstants.CreatePathName}",
            response_model=VehicleWithRelationsDTO,
            summary="Создать ТС в системе",
            description="Создание транспортных средств в системе",
        )(self.create)
        self.router.put(
            f"{AppPathConstants.UpdatePathName}",
            response_model=VehicleWithRelationsDTO,
            summary="Обновить ТС по уникальному ID",
            description="Обновление ТС по уникальному идентификатору",
        )(self.update)
        self.router.delete(
            f"{AppPathConstants.DeleteByIdPathName}",
            response_model=bool,
            summary="Удалите ТС по уникальному ID",
            description="Удаление ТС по уникальному идентификатору",
        )(self.delete)
        self.router.get(
            f"{AppPathConstants.GetByIdPathName}",
            response_model=VehicleWithRelationsDTO,
            summary="Получить ТС по уникальному ID",
            description="Получение ТС по уникальному идентификатору",
        )(self.get)
        self.router.get(
            f"{AppPathConstants.GetByValuePathName}",
            response_model=VehicleWithRelationsDTO,
            summary="Получить ТС по уникальному значению номера ТС",
            description="Получение ТС по уникальному значению номера ТС в системе",
        )(self.get_by_value)
        # Client
        self.router.get(
            f"{AppPathConstants.PaginateClientVehiclesPathName}",
            response_model=PaginationVehicleWithRelationsDTO,
            summary="Список транспортных средств клиента",
            description="Получение списка транспортных средств клиента",
        )(self.get_all_client)
        self.router.get(
            f"{AppPathConstants.GetClientVehiclesPathName}",
            response_model=List[VehicleWithRelationsDTO],
            summary="Список транспортных средств клиента",
            description="Получение списка транспортных средств клиента",
        )(self.active_client_vehicle)
        self.router.post(
            f"{AppPathConstants.AddClientVehiclePathName}",
            response_model=VehicleWithRelationsDTO,
            summary="Создать ТС в системе клиентом",
            description="Создание транспортных средств в системе клиентом",
        )(self.create_client)
        self.router.put(
            f"{AppPathConstants.UpdateClientVehiclePathName}",
            response_model=VehicleWithRelationsDTO,
            summary="Обновить ТС клиента по уникальному ID",
            description="Обновление ТС клиента по уникальному идентификатору",
        )(self.update_client)

    async def get_all(
        self, parameters: VehicleFilter = Depends(), db: AsyncSession = Depends(get_db)
    ):
        use_case = PaginateVehicleCase(db)
        try:
            return await use_case.execute(filter=parameters)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении ТС",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def get_all_client(
        self,
        parameters: VehicleClientFilter = Depends(),
        db: AsyncSession = Depends(get_db),
        user: UserWithRelationsDTO = Depends(check_client),
    ):
        use_case = PaginateClientVehicleCase(db)
        try:
            return await use_case.execute(filter=parameters, user=user)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении ТС",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def active_client_vehicle(
        self,
        parameters: VehicleClientFilter = Depends(),
        db: AsyncSession = Depends(get_db),
        user: UserWithRelationsDTO = Depends(check_client),
    ):
        use_case = AllClientVehicleCase(db)
        try:
            return await use_case.execute(filter=parameters, user=user)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении ТС",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def get(
        self, id: AppPathConstants.IDPath, db: AsyncSession = Depends(get_db)
    ):
        use_case = GetVehicleByIdCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении ТС по id",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def create(
        self,
        dto: VehicleCDTO = Depends(),
        file: Optional[UploadFile] = File(default=None),
        db: AsyncSession = Depends(get_db),
    ):
        use_case = CreateVehicleCase(db)
        try:
            return await use_case.execute(dto=dto, file=file)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании ТС",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def create_client(
        self,
        dto: VehicleCDTO = Depends(),
        file: Optional[UploadFile] = File(default=None),
        db: AsyncSession = Depends(get_db),
        user: UserWithRelationsDTO = Depends(check_client),
    ):
        use_case = AddClientVehicleCase(db)
        try:
            return await use_case.execute(dto=dto, file=file, user=user)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании ТС",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def update(
        self,
        id: AppPathConstants.IDPath,
        dto: VehicleCDTO = Depends(),
        file: Optional[UploadFile] = File(default=None),
        db: AsyncSession = Depends(get_db),
    ):
        use_case = UpdateVehicleCase(db)
        try:
            return await use_case.execute(id=id, dto=dto, file=file)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при обновлении бизнес процесса",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def update_client(
        self,
        id: AppPathConstants.IDPath,
        dto: VehicleCDTO = Depends(),
        file: Optional[UploadFile] = File(default=None),
        db: AsyncSession = Depends(get_db),
        user: UserWithRelationsDTO = Depends(check_client),
    ):
        use_case = EditClientVehicleCase(db)
        try:
            return await use_case.execute(id=id, dto=dto, file=file, user=user)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при обновлении ТС",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def delete(
        self, id: AppPathConstants.IDPath, db: AsyncSession = Depends(get_db)
    ):
        use_case = DeleteVehicleCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при удалении ТС",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def get_by_value(
        self, value: AppPathConstants.ValuePath, db: AsyncSession = Depends(get_db)
    ):
        use_case = GetVehicleByValueCase(db)
        try:
            return await use_case.execute(value=value)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении ТС по значению номера ТС",
                extra={"value": value, "details": str(exc)},
                is_custom=True,
            )
