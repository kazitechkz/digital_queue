from typing import List

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.role.role_dto import RoleCDTO, RoleRDTO
from app.adapters.repositories.role.role_repository import RoleRepository
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class CreateRoleCase(BaseUseCase[RoleRDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = RoleRepository(db)

    async def execute(self, dto: RoleCDTO) -> RoleRDTO:
        obj = await self.validate(dto=dto)
        data = await self.repository.create(obj=obj)
        return RoleRDTO.from_orm(data)

    async def validate(self, dto: RoleCDTO):
        existed = await self.repository.get_first_with_filters(
            filters=[func.lower(self.repository.model.value) == dto.value.lower()]
        )
        if existed:
            raise AppExceptionResponse.bad_request(
                "Роль с таким значением уже существует"
            )
        return self.repository.model(**dto.dict())
