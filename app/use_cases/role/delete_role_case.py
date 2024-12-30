from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.role.role_dto import RoleCDTO, RoleRDTO
from app.adapters.repositories.role.role_repository import RoleRepository
from app.core.app_exception_response import AppExceptionResponse
from app.shared.db_constants import AppDbValueConstants
from app.use_cases.base_case import BaseUseCase


class DeleteRoleCase(BaseUseCase[bool]):
    def __init__(self, db: AsyncSession):
        self.repository = RoleRepository(db)

    async def execute(self, id: int) -> bool:
        await self.validate(id=id)
        data = await self.repository.delete(id=id)
        return data

    async def validate(self, id: int):
        existed = await self.repository.get(id=id)
        if existed is None:
            raise AppExceptionResponse.not_found(message="Роль не найдена")
        if existed.value in AppDbValueConstants.IMMUTABLE_ROLES:
            raise AppExceptionResponse.bad_request(message="Роль нельзя удалять")
