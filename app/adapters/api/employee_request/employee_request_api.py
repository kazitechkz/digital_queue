from typing import Optional
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.employee_request.employee_request_dto import EmployeeRequestWithRelationsDTO, EmployeeRequestCDTO, \
    EmployeeRequestClientCDTO
from app.adapters.dto.pagination_dto import \
    PaginationEmployeeRequestWithRelationsDTO
from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.adapters.filters.employee_request.client.employee_request_client_filter import EmployeeRequestClientFilter
from app.core.api_middleware_core import check_client, check_legal_client, check_individual_client
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.database import get_db
from app.shared.path_constants import AppPathConstants
from app.use_cases.employee_request.client.create_employee_request_case import CreateEmployeeRequestCase
from app.use_cases.employee_request.client.delete_employee_request_case import DeleteEmployeeRequestCase
from app.use_cases.employee_request.client.paginate_employee_request_case import PaginateEmployeeRequestCase
from app.use_cases.employee_request.client.update_employee_request_case import UpdateEmployeeRequestCase


class EmployeeRequestApi:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            f"{AppPathConstants.PaginateClientEmployeeRequestPathName}",
            response_model=PaginationEmployeeRequestWithRelationsDTO,
            summary="Список заявок",
            description="Получение списка заявок",
        )(self.get_all)
        self.router.post(
            f"{AppPathConstants.CreateClientEmployeeRequestPathName}",
            response_model=EmployeeRequestWithRelationsDTO,
            summary="Создать заявку",
            description="Создание заявки в системе",
        )(self.create)
        self.router.put(
            f"{AppPathConstants.UpdateClientEmployeeRequestPathName}",
            response_model=EmployeeRequestWithRelationsDTO,
            summary="Обновить заявки",
            description="Обновление заявки",
        )(self.update)
        self.router.delete(
            f"{AppPathConstants.DeleteClientEmployeeRequestPathName}",
            response_model=bool,
            summary="Удалите заявку по уникальному ID",
            description="Удаление заявок по уникальному идентификатору",
        )(self.delete)
        #client


    async def get_all(
        self,
        parameters: EmployeeRequestClientFilter = Depends(),
        db: AsyncSession = Depends(get_db),
        user:UserWithRelationsDTO = Depends(check_client)
    ):
        use_case = PaginateEmployeeRequestCase(db)
        try:
            return await use_case.execute(filter=parameters,user=user)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении заявок",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def create(
        self,
        dto: EmployeeRequestCDTO,
        db: AsyncSession = Depends(get_db),
        user: UserWithRelationsDTO = Depends(check_legal_client)
    ):
        use_case = CreateEmployeeRequestCase(db)
        try:
            return await use_case.execute(dto=dto,user=user)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании заявки",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def update(
        self,
        id: AppPathConstants.IDPath,
        dto: EmployeeRequestClientCDTO,
        db: AsyncSession = Depends(get_db),
        user: UserWithRelationsDTO = Depends(check_individual_client)
    ):
        use_case = UpdateEmployeeRequestCase(db)
        try:
            return await use_case.execute(id=id, dto=dto, user=user)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при обновлении заявки",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def delete(
        self, id: AppPathConstants.IDPath, db: AsyncSession = Depends(get_db),
            user: UserWithRelationsDTO = Depends(check_legal_client)
    ):
        use_case = DeleteEmployeeRequestCase(db)
        try:
            return await use_case.execute(id=id,user=user)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при удалении заявки",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )


