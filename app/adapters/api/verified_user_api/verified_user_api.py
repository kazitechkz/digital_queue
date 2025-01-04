from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationVerifiedUserWithRelationsDTO
from app.adapters.dto.verified_user.verified_user_dto import (
    VerifiedUserCDTO,
    VerifiedUserRDTO,
    VerifiedUserWithRelationsDTO,
)
from app.adapters.filters.verified_user.verified_user_filter import VerifiedUserFilter
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.database import get_db
from app.shared.path_constants import AppPathConstants
from app.use_cases.verified_user.create_verified_user_case import CreateVerifiedUserCase
from app.use_cases.verified_user.delete_verified_user_case import DeleteVerifiedUserCase
from app.use_cases.verified_user.get_verified_user_by_id_case import (
    GetVerifiedUserByIdCase,
)
from app.use_cases.verified_user.get_verified_user_by_value_case import (
    GetVerifiedUserByValueCase,
)
from app.use_cases.verified_user.paginate_verified_user_case import (
    PaginateVerifiedUserCase,
)
from app.use_cases.verified_user.update_verified_user_case import UpdateVerifiedUserCase


class VerifiedUserApi:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            "/",
            response_model=PaginationVerifiedUserWithRelationsDTO,
            summary="Список верифицированных пользователей",
            description="Получение списка верифицированных пользователей",
        )(self.get_all)
        self.router.post(
            "/create",
            response_model=VerifiedUserWithRelationsDTO,
            summary="Создать цвет ТС",
            description="Создание верифицированного пользователей",
        )(self.create)
        self.router.put(
            "/update/{id}",
            response_model=VerifiedUserWithRelationsDTO,
            summary="Обновить цвет ТС по уникальному ID",
            description="Обновление верифицированного пользователей по уникальному идентификатору",
        )(self.update)
        self.router.delete(
            "/delete/{id}",
            response_model=bool,
            summary="Удалите цвет ТС по уникальному ID",
            description="Удаление верифицированного пользователей по уникальному идентификатору",
        )(self.delete)
        self.router.get(
            "/get/{id}",
            response_model=VerifiedUserWithRelationsDTO,
            summary="Получить цвет ТС по уникальному ID",
            description="Получение верифицированного пользователей по уникальному идентификатору",
        )(self.get)
        self.router.get(
            "/get-by-value/{value}",
            response_model=VerifiedUserWithRelationsDTO,
            summary="Получить цвет ТС по уникальному значению",
            description="Получение верифицированного пользователей по уникальному значению ИИН СИД, описанию или отказу",
        )(self.get_by_value)

    async def get_all(
        self,
        parameters: VerifiedUserFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ):
        use_case = PaginateVerifiedUserCase(db)
        try:
            return await use_case.execute(filter=parameters)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении всех верифицированных пользователей",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def get(
        self, id: AppPathConstants.IDPath, db: AsyncSession = Depends(get_db)
    ):
        use_case = GetVerifiedUserByIdCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении верифицированного пользователей по значению",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def create(self, dto: VerifiedUserCDTO, db: AsyncSession = Depends(get_db)):
        use_case = CreateVerifiedUserCase(db)
        try:
            return await use_case.execute(dto=dto)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании верифицированного пользователей",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def update(
        self,
        id: AppPathConstants.IDPath,
        dto: VerifiedUserCDTO,
        db: AsyncSession = Depends(get_db),
    ):
        use_case = UpdateVerifiedUserCase(db)
        try:
            return await use_case.execute(id=id, dto=dto)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании верифицированного пользователей",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def delete(
        self, id: AppPathConstants.IDPath, db: AsyncSession = Depends(get_db)
    ):
        use_case = DeleteVerifiedUserCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании верифицированного пользователей",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def get_by_value(
        self, value: AppPathConstants.ValuePath, db: AsyncSession = Depends(get_db)
    ):
        use_case = GetVerifiedUserByValueCase(db)
        try:
            return await use_case.execute(value=value)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении верифицированного пользователей по значению",
                extra={"value": value, "details": str(exc)},
                is_custom=True,
            )
