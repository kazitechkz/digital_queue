from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationUserWithRelationsDTO
from app.adapters.dto.user.user_dto import UserCDTO, UserWithRelationsDTO
from app.adapters.filters.user.user_filter import UserFilter
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.database import get_db
from app.shared.app_file_constants import AppFileExtensionConstants
from app.shared.path_constants import AppPathConstants
from app.use_cases.file.save_file_case import SaveFileCase
from app.use_cases.user.create_user_case import CreateUserCase
from app.use_cases.user.delete_user_case import DeleteUserCase
from app.use_cases.user.get_user_by_id_case import GetUserByIdCase
from app.use_cases.user.get_user_by_value_case import GetUserByValueCase
from app.use_cases.user.paginate_user_case import PaginateUserCase
from app.use_cases.user.update_user_case import UpdateUserCase


class UserApi:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            "/",
            response_model=PaginationUserWithRelationsDTO,
            summary="Список пользователей",
            description="Получение списка пользователей",
        )(self.get_all)
        self.router.post(
            "/create",
            response_model=UserWithRelationsDTO,
            summary="Создать пользователя в системе",
            description="Создание пользователей в системе",
        )(self.create)
        self.router.put(
            "/update/{id}",
            response_model=UserWithRelationsDTO,
            summary="Обновить пользователя по уникальному ID",
            description="Обновление пользователя по уникальному идентификатору",
        )(self.update)
        self.router.delete(
            "/delete/{id}",
            response_model=bool,
            summary="Удалите пользователя по уникальному ID",
            description="Удаление пользователя по уникальному идентификатору",
        )(self.delete)
        self.router.get(
            "/get/{id}",
            response_model=UserWithRelationsDTO,
            summary="Получить пользователя по уникальному ID",
            description="Получение пользователя по уникальному идентификатору",
        )(self.get)
        self.router.get(
            "/get-by-value/{value}",
            response_model=UserWithRelationsDTO,
            summary="Получить пользователя по уникальному значению ИИН, НИКНЕЙМУ ИЛИ АЙДИ KEYCLOAK",
            description="Получение пользователя по уникальному значению в системе ИИН, НИКНЕЙМУ ИЛИ АЙДИ KEYCLOAK",
        )(self.get_by_value)

    async def get_all(
        self, parameters: UserFilter = Depends(), db: AsyncSession = Depends(get_db)
    ):
        use_case = PaginateUserCase(db)
        try:
            return await use_case.execute(filter=parameters)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении пользователя",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def get(
        self, id: AppPathConstants.IDPath, db: AsyncSession = Depends(get_db)
    ):
        use_case = GetUserByIdCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении пользователя по id",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def create(
        self,
        dto: UserCDTO = Depends(),
        file: Optional[UploadFile] = File(default=None),
        db: AsyncSession = Depends(get_db),
    ):
        use_case = CreateUserCase(db)
        try:
            return await use_case.execute(dto=dto, file=file)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании пользователя",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def update(
        self,
        id: AppPathConstants.IDPath,
        dto: UserCDTO = Depends(),
        file: Optional[UploadFile] = File(default=None),
        db: AsyncSession = Depends(get_db),
    ):
        use_case = UpdateUserCase(db)
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

    async def delete(
        self, id: AppPathConstants.IDPath, db: AsyncSession = Depends(get_db)
    ):
        use_case = DeleteUserCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при удалении пользователя",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def get_by_value(
        self, value: AppPathConstants.ValuePath, db: AsyncSession = Depends(get_db)
    ):
        use_case = GetUserByValueCase(db)
        try:
            return await use_case.execute(value=value)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении пользователя по значению SAP ID",
                extra={"value": value, "details": str(exc)},
                is_custom=True,
            )
