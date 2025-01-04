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


class CreateOperationCase(BaseUseCase[OperationWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = OperationRepository(db)
        self.role_repository = RoleRepository(db)

    async def execute(self, dto: OperationCDTO) -> OperationWithRelationsDTO:
        obj = await self.validate(dto=dto)
        data = await self.repository.create(obj=obj)
        if not data:
            raise AppExceptionResponse.not_found("Процесс не найден")
        else:
            existed = await self.repository.get(
                id=data.id,
                options=self.repository.default_relationships(),
            )
        return OperationWithRelationsDTO.from_orm(existed)

    async def validate(self, dto: OperationCDTO):
        dict_dto = dto.dict()
        existed = await self.repository.get_first_with_filters(
            filters=[func.lower(self.repository.model.value) == dto.value.lower()]
        )
        if existed:
            raise AppExceptionResponse.bad_request(
                "Процесс с таким значением уже существует"
            )
        if dto.next_id:
            next_obj = await self.repository.get(id=dto.next_id)
            if not next_obj:
                raise AppExceptionResponse.bad_request("Следующий шаг не найден")
            else:
                dict_dto["next_value"] = next_obj.value
        if dto.prev_id:
            prev_obj = await self.repository.get(id=dto.prev_id)
            if not prev_obj:
                raise AppExceptionResponse.bad_request("Предыдущий шаг не найден")
            else:
                dict_dto["prev_value"] = prev_obj.value
        role = await self.role_repository.get(dto.role_id)
        if not role:
            raise AppExceptionResponse.bad_request("Роль не найдена")
        if (
            role.value != dto.role_value
            or role.keycloak_value != dto.role_keycloak_value
        ):
            raise AppExceptionResponse.bad_request("Данные роли не совпадают")
        return self.repository.model(**dict_dto)
