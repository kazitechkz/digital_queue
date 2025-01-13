from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.role.role_dto import RoleCDTO, RoleRDTO
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.database import get_db
from app.shared.path_constants import AppPathConstants
from app.use_cases.role.all_role_case import AllRoleCase
from app.use_cases.role.create_role_case import CreateRoleCase
from app.use_cases.role.delete_role_case import DeleteRoleCase
from app.use_cases.role.get_role_by_id_case import GetRoleByIdCase
from app.use_cases.role.get_role_by_value_case import GetRoleByValueCase
from app.use_cases.role.update_role_case import UpdateRoleCase


class RoleApi:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            f"{AppPathConstants.IndexPathName}",
            response_model=list[RoleRDTO],
            summary="Список ролей",
            description="Получение списка ролей",
        )(self.get_all)
        self.router.post(
            f"{AppPathConstants.CreatePathName}",
            response_model=RoleRDTO,
            summary="Создать роль",
            description="Создание роли",
        )(self.create)
        self.router.put(
            f"{AppPathConstants.UpdatePathName}",
            response_model=RoleRDTO,
            summary="Обновить роль по уникальному ID",
            description="Обновление роли по уникальному идентификатору",
        )(self.update)
        self.router.delete(
            f"{AppPathConstants.DeleteByIdPathName}",
            response_model=bool,
            summary="Удалите роль по уникальному ID",
            description="Удаление роли по уникальному идентификатору",
        )(self.delete)
        self.router.get(
            f"{AppPathConstants.GetByIdPathName}",
            response_model=RoleRDTO,
            summary="Получить роль по уникальному ID",
            description="Получение роли по уникальному идентификатору",
        )(self.get)
        self.router.get(
            f"{AppPathConstants.GetByValuePathName}",
            response_model=RoleRDTO,
            summary="Получить роль по уникальному значению",
            description="Получение роли по уникальному значению",
        )(self.get_by_value)

    async def get_all(self, db: AsyncSession = Depends(get_db)):
        use_case = AllRoleCase(db)
        try:
            return await use_case.execute()
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении всех ролей",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def get(
        self, id: AppPathConstants.IDPath, db: AsyncSession = Depends(get_db)
    ):
        use_case = GetRoleByIdCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении роли по значению",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def create(self, dto: RoleCDTO, db: AsyncSession = Depends(get_db)):
        use_case = CreateRoleCase(db)
        try:
            return await use_case.execute(dto=dto)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании роли",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def update(
        self,
        id: AppPathConstants.IDPath,
        dto: RoleCDTO,
        db: AsyncSession = Depends(get_db),
    ):
        use_case = UpdateRoleCase(db)
        try:
            return await use_case.execute(id=id, dto=dto)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании роли",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def delete(
        self, id: AppPathConstants.IDPath, db: AsyncSession = Depends(get_db)
    ):
        use_case = DeleteRoleCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании роли",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )

    async def get_by_value(
        self, value: AppPathConstants.ValuePath, db: AsyncSession = Depends(get_db)
    ):
        use_case = GetRoleByValueCase(db)
        try:
            return await use_case.execute(value=value)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении роли по значению",
                extra={"value": value, "details": str(exc)},
                is_custom=True,
            )
