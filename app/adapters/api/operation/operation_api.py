from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.operation.operation_dto import (
    OperationCDTO,
    OperationWithRelationsDTO,
)
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.database import get_db
from app.shared.path_constants import AppPathConstants
from app.use_cases.operation.all_operation_case import AllOperationCase
from app.use_cases.operation.create_operation_case import CreateOperationCase
from app.use_cases.operation.delete_operation_case import DeleteOperationCase
from app.use_cases.operation.get_operation_by_id_case import GetOperationByIdCase
from app.use_cases.operation.get_operation_by_value_case import GetOperationByValueCase
from app.use_cases.operation.update_operation_case import UpdateOperationCase


class OperationApi:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            "/",
            response_model=list[OperationWithRelationsDTO],
            summary="Список бизнес процессов",
            description="Получение списка бизнес процессов",
        )(self.get_all)
        self.router.post(
            "/create",
            response_model=OperationWithRelationsDTO,
            summary="Создать бизнес процесс",
            description="Создание бизнес процесса",
        )(self.create)
        self.router.put(
            "/update/{id}",
            response_model=OperationWithRelationsDTO,
            summary="Обновить бизнес процесс по уникальному ID",
            description="Обновление бизнес процесса по уникальному идентификатору",
        )(self.update)
        self.router.delete(
            "/delete/{id}",
            response_model=bool,
            summary="Удалите бизнес процесс по уникальному ID",
            description="Удаление бизнес процесса по уникальному идентификатору",
        )(self.delete)
        self.router.get(
            "/get/{id}",
            response_model=OperationWithRelationsDTO,
            summary="Получить бизнес процесс по уникальному ID",
            description="Получение бизнес процесса по уникальному идентификатору",
        )(self.get)
        self.router.get(
            "/get-by-value/{value}",
            response_model=OperationWithRelationsDTO,
            summary="Получить бизнес процесс по уникальному значению",
            description="Получение бизнес процесса по уникальному значению",
        )(self.get_by_value)

    async def get_all(self, db: AsyncSession = Depends(get_db)):
        use_case = AllOperationCase(db)
        try:
            return await use_case.execute()
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении бизнес процессов",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def get(
        self, id: AppPathConstants.IDPath, db: AsyncSession = Depends(get_db)
    ):
        use_case = GetOperationByIdCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении бизнес процессов по id",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def create(self, dto: OperationCDTO, db: AsyncSession = Depends(get_db)):
        use_case = CreateOperationCase(db)
        try:
            return await use_case.execute(dto=dto)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании бизнес процесса",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def update(
        self,
        id: AppPathConstants.IDPath,
        dto: OperationCDTO,
        db: AsyncSession = Depends(get_db),
    ):
        use_case = UpdateOperationCase(db)
        try:
            return await use_case.execute(id=id, dto=dto)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при обновлении бизнес процесса",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def delete(
        self, id: AppPathConstants.IDPath, db: AsyncSession = Depends(get_db)
    ):
        use_case = DeleteOperationCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при удалении бизнес процесса",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    #
    async def get_by_value(
        self, value: AppPathConstants.ValuePath, db: AsyncSession = Depends(get_db)
    ):
        use_case = GetOperationByValueCase(db)
        try:
            return await use_case.execute(value=value)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении бизнес процесса по значению",
                extra={"value": value, "details": str(exc)},
                is_custom=True,
            )
