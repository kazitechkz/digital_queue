from typing import List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.organization.organization_dto import (
    OrganizationCDTO,
    OrganizationWithRelationsDTO,
)
from app.adapters.dto.pagination_dto import PaginationOrganizationWithRelationsDTO
from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.adapters.filters.organization.client.organization_client_filter import (
    OrganizationClientFilter,
)
from app.adapters.filters.organization.organization_filter import OrganizationFilter
from app.core.api_middleware_core import check_legal_client
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.database import get_db
from app.shared.path_constants import AppPathConstants
from app.use_cases.organization.client.add_client_organization_case import (
    AddClientOrganizationCase,
)
from app.use_cases.organization.client.all_client_organization_case import (
    AllClientOrganizationCase,
)
from app.use_cases.organization.client.edit_client_organization_case import (
    EditClientOrganizationCase,
)
from app.use_cases.organization.client.pagination_client_organization_case import (
    PaginateClientOrganizationCase,
)
from app.use_cases.organization.create_organization_case import CreateOrganizationCase
from app.use_cases.organization.delete_organization_case import DeleteOrganizationCase
from app.use_cases.organization.get_organization_by_id_case import (
    GetOrganizationByIdCase,
)
from app.use_cases.organization.get_organization_by_value_case import (
    GetOrganizationByValueCase,
)
from app.use_cases.organization.paginate_organization_case import (
    PaginateOrganizationCase,
)
from app.use_cases.organization.update_organization_case import UpdateOrganizationCase


class OrganizationApi:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            f"{AppPathConstants.IndexPathName}",
            response_model=PaginationOrganizationWithRelationsDTO,
            summary="Список организаций",
            description="Получение списка организаций",
        )(self.get_all)
        self.router.post(
            f"{AppPathConstants.CreatePathName}",
            response_model=OrganizationWithRelationsDTO,
            summary="Создать организацию в системе",
            description="Создание организаций в системе",
        )(self.create)
        self.router.put(
            f"{AppPathConstants.UpdatePathName}",
            response_model=OrganizationWithRelationsDTO,
            summary="Обновить организацию по уникальному ID",
            description="Обновление организации по уникальному идентификатору",
        )(self.update)
        self.router.delete(
            f"{AppPathConstants.DeleteByIdPathName}",
            response_model=bool,
            summary="Удалите организацию по уникальному ID",
            description="Удаление организации по уникальному идентификатору",
        )(self.delete)
        self.router.get(
            f"{AppPathConstants.GetByIdPathName}",
            response_model=OrganizationWithRelationsDTO,
            summary="Получить организацию по уникальному ID",
            description="Получение организации по уникальному идентификатору",
        )(self.get)
        self.router.get(
            f"{AppPathConstants.GetByValuePathName}",
            response_model=OrganizationWithRelationsDTO,
            summary="Получить организацию по уникальному значению БИН",
            description="Получение организации по уникальному значению БИН в системе",
        )(self.get_by_value)
        # Client
        self.router.get(
            f"{AppPathConstants.PaginateClientOrganizationPathName}",
            response_model=PaginationOrganizationWithRelationsDTO,
            summary="Список организаций клиента",
            description="Получение списка организаций клиента",
        )(self.get_all_client)
        self.router.get(
            f"{AppPathConstants.AllClientOrganizationPathName}",
            response_model=List[OrganizationWithRelationsDTO],
            summary="Список организаций клиента",
            description="Получение списка организаций клиента",
        )(self.get_active_client)
        self.router.post(
            f"{AppPathConstants.AddClientOrganizationPathName}",
            response_model=OrganizationWithRelationsDTO,
            summary="Создать организацию в системе",
            description="Создание организаций в системе",
        )(self.create_client)
        self.router.put(
            f"{AppPathConstants.UpdateClientOrganizationPathName}",
            response_model=OrganizationWithRelationsDTO,
            summary="Обновить организацию по уникальному ID",
            description="Обновление организации по уникальному идентификатору",
        )(self.update_client)

    async def get_all(
        self,
        parameters: OrganizationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ):
        use_case = PaginateOrganizationCase(db)
        try:
            return await use_case.execute(filter=parameters)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении организации",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def get_all_client(
        self,
        parameters: OrganizationClientFilter = Depends(),
        db: AsyncSession = Depends(get_db),
        user: UserWithRelationsDTO = Depends(check_legal_client),
    ):
        use_case = PaginateClientOrganizationCase(db)
        try:
            return await use_case.execute(filter=parameters, client_id=user.id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении организации",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def get_active_client(
        self,
        parameters: OrganizationClientFilter = Depends(),
        db: AsyncSession = Depends(get_db),
        user: UserWithRelationsDTO = Depends(check_legal_client),
    ):
        use_case = AllClientOrganizationCase(db)
        try:
            return await use_case.execute(filter=parameters, client_id=user.id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении организации",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def get(
        self, id: AppPathConstants.IDPath, db: AsyncSession = Depends(get_db)
    ):
        use_case = GetOrganizationByIdCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении организации по id",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def create(
        self,
        dto: OrganizationCDTO = Depends(),
        file: Optional[UploadFile] = File(default=None),
        db: AsyncSession = Depends(get_db),
    ):
        use_case = CreateOrganizationCase(db)
        try:
            return await use_case.execute(dto=dto, file=file)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании организации",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def create_client(
        self,
        dto: OrganizationCDTO = Depends(),
        file: Optional[UploadFile] = File(default=None),
        db: AsyncSession = Depends(get_db),
        user: UserWithRelationsDTO = Depends(check_legal_client),
    ):
        use_case = AddClientOrganizationCase(db)
        try:
            return await use_case.execute(dto=dto, file=file, user=user)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании организации",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def update(
        self,
        id: AppPathConstants.IDPath,
        dto: OrganizationCDTO = Depends(),
        file: Optional[UploadFile] = File(default=None),
        db: AsyncSession = Depends(get_db),
    ):
        use_case = UpdateOrganizationCase(db)
        try:
            return await use_case.execute(id=id, dto=dto, file=file)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при обновлении организации",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def update_client(
        self,
        id: AppPathConstants.IDPath,
        dto: OrganizationCDTO = Depends(),
        file: Optional[UploadFile] = File(default=None),
        db: AsyncSession = Depends(get_db),
        user: UserWithRelationsDTO = Depends(check_legal_client),
    ):
        use_case = EditClientOrganizationCase(db)
        try:
            return await use_case.execute(id=id, dto=dto, file=file, user=user)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при обновлении организации",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def delete(
        self, id: AppPathConstants.IDPath, db: AsyncSession = Depends(get_db)
    ):
        use_case = DeleteOrganizationCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при удалении организации",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def get_by_value(
        self, value: AppPathConstants.ValuePath, db: AsyncSession = Depends(get_db)
    ):
        use_case = GetOrganizationByValueCase(db)
        try:
            return await use_case.execute(value=value)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении организации по значению БИН",
                extra={"value": value, "details": str(exc)},
                is_custom=True,
            )
