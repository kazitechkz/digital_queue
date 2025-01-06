from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.user_type.user_type_dto import UserTypeCDTO, UserTypeRDTO
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.database import get_db
from app.shared.path_constants import AppPathConstants
from app.use_cases.user_type.all_user_type_case import AllUserTypeCase
from app.use_cases.user_type.create_user_type_case import CreateUserTypeCase
from app.use_cases.user_type.delete_user_type_case import DeleteUserTypeCase
from app.use_cases.user_type.get_user_type_by_id_case import \
    GetUserTypeByIdCase
from app.use_cases.user_type.get_user_type_by_value_case import \
    GetUserTypeByValueCase
from app.use_cases.user_type.update_user_type_case import UpdateUserTypeCase


class UserTypeApi:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            f"{AppPathConstants.IndexPathName}",
            response_model=list[UserTypeRDTO],
            summary="Список типов пользователя",
            description="Получение списка типов пользователя",
        )(self.get_all)
        self.router.post(
            f"{AppPathConstants.CreatePathName}",
            response_model=UserTypeRDTO,
            summary="Создать тип пользователя",
            description="Создание типа пользователя",
        )(self.create)
        self.router.put(
            f"{AppPathConstants.UpdatePathName}",
            response_model=UserTypeRDTO,
            summary="Обновить тип пользователя по уникальному ID",
            description="Обновление типа пользователя по уникальному идентификатору",
        )(self.update)
        self.router.delete(
            f"{AppPathConstants.DeleteByIdPathName}",
            response_model=bool,
            summary="Удалите тип пользователя по уникальному ID",
            description="Удаление типа пользователя по уникальному идентификатору",
        )(self.delete)
        self.router.get(
            f"{AppPathConstants.GetByIdPathName}",
            response_model=UserTypeRDTO,
            summary="Получить тип пользователя по уникальному ID",
            description="Получение типа пользователя по уникальному идентификатору",
        )(self.get)
        self.router.get(
            f"{AppPathConstants.GetByValuePathName}",
            response_model=UserTypeRDTO,
            summary="Получить тип пользователя по уникальному значению",
            description="Получение типа пользователя по уникальному значению",
        )(self.get_by_value)

    async def get_all(self, db: AsyncSession = Depends(get_db)):
        use_case = AllUserTypeCase(db)
        try:
            return await use_case.execute()
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении всех типов пользователя",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def get(
        self, id: AppPathConstants.IDPath, db: AsyncSession = Depends(get_db)
    ):
        use_case = GetUserTypeByIdCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении типа пользователя по значению",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def create(self, dto: UserTypeCDTO, db: AsyncSession = Depends(get_db)):
        use_case = CreateUserTypeCase(db)
        try:
            return await use_case.execute(dto=dto)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании типа пользователя",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def update(
        self,
        id: AppPathConstants.IDPath,
        dto: UserTypeCDTO,
        db: AsyncSession = Depends(get_db),
    ):
        use_case = UpdateUserTypeCase(db)
        try:
            return await use_case.execute(id=id, dto=dto)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании типа пользователя",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def delete(
        self, id: AppPathConstants.IDPath, db: AsyncSession = Depends(get_db)
    ):
        use_case = DeleteUserTypeCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании типа пользователя",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def get_by_value(
        self, value: AppPathConstants.ValuePath, db: AsyncSession = Depends(get_db)
    ):
        use_case = GetUserTypeByValueCase(db)
        try:
            return await use_case.execute(value=value)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении типа пользователя по значению",
                extra={"value": value, "details": str(exc)},
                is_custom=True,
            )
