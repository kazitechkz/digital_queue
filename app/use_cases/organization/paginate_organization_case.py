from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.organization.organization_dto import \
    OrganizationWithRelationsDTO
from app.adapters.dto.pagination_dto import \
    PaginationOrganizationWithRelationsDTO
from app.adapters.filters.organization.organization_filter import \
    OrganizationFilter
from app.adapters.repositories.organization.organization_repository import \
    OrganizationRepository
from app.use_cases.base_case import BaseUseCase


class PaginateOrganizationCase(BaseUseCase[PaginationOrganizationWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = OrganizationRepository(db)

    async def execute(
        self, filter: OrganizationFilter
    ) -> PaginationOrganizationWithRelationsDTO:
        models = await self.repository.paginate(
            dto=OrganizationWithRelationsDTO,
            page=filter.page,
            per_page=filter.per_page,
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            options=self.repository.default_relationships(),
            filters=filter.apply(),
        )
        return models

    async def validate(self):
        pass
