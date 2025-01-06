from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.organization_employee.organization_employee_dto import (
    OrganizationEmployeeCDTO, OrganizationEmployeeWithRelationsDTO)
from app.adapters.dto.pagination_dto import \
    PaginationOrganizationEmployeeWithRelationsDTO
from app.adapters.filters.organization_employee.organization_employee_filter import \
    OrganizationEmployeeFilter
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.database import get_db
from app.shared.path_constants import AppPathConstants
from app.use_cases.organization_employee.create_organization_employee_case import \
    CreateOrganizationEmployeeCase
from app.use_cases.organization_employee.delete_organization_employee_case import \
    DeleteOrganizationEmployeeCase
from app.use_cases.organization_employee.get_organization_employee_by_id_case import \
    GetOrganizationEmployeeByIdCase
from app.use_cases.organization_employee.get_organization_employee_by_value_case import \
    GetOrganizationEmployeeByValueCase
from app.use_cases.organization_employee.paginate_organization_employee_case import \
    PaginateOrganizationEmployeeCase
from app.use_cases.organization_employee.update_organization_employee_case import \
    UpdateOrganizationEmployeeCase


class OrganizationEmployeeApi:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            f"{AppPathConstants.IndexPathName}",
            response_model=PaginationOrganizationEmployeeWithRelationsDTO,
            summary="Список работников организаций",
            description="Получение списка работников организаций",
        )(self.get_all)
        self.router.post(
            f"{AppPathConstants.CreatePathName}",
            response_model=OrganizationEmployeeWithRelationsDTO,
            summary="Создать работников организаций в системе",
            description="Создание работников организаций в системе",
        )(self.create)
        self.router.put(
            f"{AppPathConstants.UpdatePathName}",
            response_model=OrganizationEmployeeWithRelationsDTO,
            summary="Обновить работников организаций по уникальному ID",
            description="Обновление работников организаций по уникальному идентификатору",
        )(self.update)
        self.router.delete(
            f"{AppPathConstants.DeleteByIdPathName}",
            response_model=bool,
            summary="Удалите работников организаций по уникальному ID",
            description="Удаление работников организаций по уникальному идентификатору",
        )(self.delete)
        self.router.get(
            f"{AppPathConstants.GetByIdPathName}",
            response_model=OrganizationEmployeeWithRelationsDTO,
            summary="Получить работников организаций по уникальному ID",
            description="Получение работников организаций по уникальному идентификатору",
        )(self.get)
        self.router.get(
            f"{AppPathConstants.GetByValuePathName}",
            response_model=OrganizationEmployeeWithRelationsDTO,
            summary="Получить работников организаций по уникальному значению БИН или SID",
            description="Получение работников организаций по уникальному значению БИН или SID в системе",
        )(self.get_by_value)

    async def get_all(
        self,
        parameters: OrganizationEmployeeFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ):
        use_case = PaginateOrganizationEmployeeCase(db)
        try:
            return await use_case.execute(filter=parameters)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении работников организаций",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def get(
        self, id: AppPathConstants.IDPath, db: AsyncSession = Depends(get_db)
    ):
        use_case = GetOrganizationEmployeeByIdCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении работников организаций по id",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def create(
        self,
        dto: OrganizationEmployeeCDTO = Depends(),
        file: Optional[UploadFile] = File(default=None),
        db: AsyncSession = Depends(get_db),
    ):
        use_case = CreateOrganizationEmployeeCase(db)
        try:
            return await use_case.execute(dto=dto, file=file)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании работников организаций",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def update(
        self,
        id: AppPathConstants.IDPath,
        dto: OrganizationEmployeeCDTO = Depends(),
        file: Optional[UploadFile] = File(default=None),
        db: AsyncSession = Depends(get_db),
    ):
        use_case = UpdateOrganizationEmployeeCase(db)
        try:
            return await use_case.execute(id=id, dto=dto, file=file)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при обновлении работников организаций",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def delete(
        self, id: AppPathConstants.IDPath, db: AsyncSession = Depends(get_db)
    ):
        use_case = DeleteOrganizationEmployeeCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при удалении работников организаций",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def get_by_value(
        self, value: AppPathConstants.ValuePath, db: AsyncSession = Depends(get_db)
    ):
        use_case = GetOrganizationEmployeeByValueCase(db)
        try:
            return await use_case.execute(value=value)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении работников организаций по значению БИН или SID",
                extra={"value": value, "details": str(exc)},
                is_custom=True,
            )
