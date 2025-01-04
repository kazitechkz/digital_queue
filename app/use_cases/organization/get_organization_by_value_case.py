from sqlalchemy import and_, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.organization.organization_dto import OrganizationWithRelationsDTO
from app.adapters.repositories.organization.organization_repository import (
    OrganizationRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class GetOrganizationByValueCase(BaseUseCase[OrganizationWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = OrganizationRepository(db)

    async def execute(self, value: str) -> OrganizationWithRelationsDTO:
        filters = [
            or_(
                func.lower(self.repository.model.bin) == value.lower(),
            )
        ]
        model = await self.repository.get_first_with_filters(
            filters=filters,
            options=self.repository.default_relationships(),
        )
        if not model:
            raise AppExceptionResponse.not_found("Организация не найдена")
        return OrganizationWithRelationsDTO.from_orm(model)

    async def validate(self):
        pass
