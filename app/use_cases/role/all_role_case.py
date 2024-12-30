from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.role.role_dto import RoleRDTO
from app.adapters.repositories.role.role_repository import RoleRepository
from app.use_cases.base_case import BaseUseCase


class AllRoleCase(BaseUseCase[list[RoleRDTO]]):
    def __init__(self, db: AsyncSession):
        self.repository = RoleRepository(db)

    async def execute(self) -> list[RoleRDTO]:
        models = await self.repository.get_all()
        return [RoleRDTO.from_orm(model) for model in models]

    async def validate(self):
        pass
