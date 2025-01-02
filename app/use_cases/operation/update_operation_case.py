from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.dto.operation.operation_dto import (
    OperationCDTO,
    OperationWithRelationsDTO,
)
from app.adapters.repositories.operation.operation_repository import OperationRepository
from app.adapters.repositories.role.role_repository import RoleRepository
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class UpdateOperationCase(BaseUseCase[OperationWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = OperationRepository(db)
        self.role_repository = RoleRepository(db)

    async def execute(self, id: int, dto: OperationCDTO) -> OperationWithRelationsDTO:
        obj = await self.validate(id=id, dto=dto)
        data = await self.repository.update(obj=obj, dto=dto)
        if not data:
            raise AppExceptionResponse.not_found("Процесс не найден")
        else:
            existed = await self.repository.get(
                id=data.id,
                options=[
                    selectinload(self.repository.model.prev_operation),
                    selectinload(self.repository.model.next_operation),
                    selectinload(self.repository.model.role),
                ],
            )
        return OperationWithRelationsDTO.from_orm(existed)

    async def validate(self, id: int, dto: OperationCDTO):
        existed = await self.repository.get(id=id)
        if existed is None:
            raise AppExceptionResponse.not_found(message="Процесс не найден")
        if await self.repository.get_first_with_filters(
            [
                func.lower(self.repository.model.value) == dto.value.lower(),
                self.repository.model.id != id,
            ]
        ):
            raise AppExceptionResponse.bad_request(
                "Процесс с таким значением уже существует"
            )
        if dto.next_id:
            next_obj = await self.repository.get(id=dto.next_id)
            if not next_obj:
                raise AppExceptionResponse.bad_request("Процесс не найден")
            elif next_obj.value != dto.next_value:
                raise AppExceptionResponse.bad_request(
                    "Данные следующего статуса не совпадает"
                )
        if dto.prev_id:
            prev_obj = await self.repository.get(id=dto.prev_id)
            if not prev_obj:
                raise AppExceptionResponse.bad_request("Предыдущий статус не найден")
            elif prev_obj.value != dto.prev_value:
                raise AppExceptionResponse.bad_request(
                    "Данные предыдущего статуса не совпадает"
                )
        role = await self.role_repository.get(dto.role_id)
        if not role:
            raise AppExceptionResponse.bad_request("Роль не найдена")
        if (
            role.value != dto.role_value
            or role.keycloak_value != dto.role_keycloak_value
        ):
            raise AppExceptionResponse.bad_request("Данные роли не совпадают")
        return existed
