from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.role.role_dto import RoleRDTO
from app.adapters.repositories.role.role_repository import RoleRepository
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class GetRoleByIdCase(BaseUseCase[RoleRDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = RoleRepository(db)

    async def execute(self, id: int) -> RoleRDTO:
        model = await self.repository.get(id)
        if not model:
            raise AppExceptionResponse.not_found("Роль не найдена")
        return RoleRDTO.from_orm(model)

    async def validate(self):
        pass
