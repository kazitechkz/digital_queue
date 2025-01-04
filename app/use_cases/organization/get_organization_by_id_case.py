from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.organization.organization_dto import OrganizationWithRelationsDTO
from app.adapters.repositories.organization.organization_repository import (
    OrganizationRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class GetOrganizationByIdCase(BaseUseCase[OrganizationWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = OrganizationRepository(db)

    async def execute(self, id: int) -> OrganizationWithRelationsDTO:
        model = await self.repository.get(
            id,
            options=self.repository.default_relationships(),
        )
        if not model:
            raise AppExceptionResponse.not_found("Организация не найдена")
        return OrganizationWithRelationsDTO.from_orm(model)

    async def validate(self):
        pass
