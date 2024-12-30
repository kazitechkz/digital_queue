from sqlalchemy import func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.role.role_dto import RoleRDTO
from app.adapters.repositories.role.role_repository import RoleRepository
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class GetRoleByValueCase(BaseUseCase[RoleRDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = RoleRepository(db)

    async def execute(self, value: str) -> RoleRDTO:
        filters = [
            or_(
                func.lower(self.repository.model.value) == value.lower(),
                func.lower(self.repository.model.keycloak_value) == value.lower(),
            )
        ]
        model = await self.repository.get_first_with_filters(filters=filters)
        if not model:
            raise AppExceptionResponse.not_found("Роль не найдена")
        return RoleRDTO.from_orm(model)

    async def validate(self):
        pass
