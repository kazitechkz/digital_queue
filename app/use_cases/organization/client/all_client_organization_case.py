from sqlalchemy.ext.asyncio import AsyncSession
from app.adapters.dto.organization.organization_dto import OrganizationWithRelationsDTO
from app.adapters.filters.organization.client.organization_client_filter import OrganizationClientFilter
from app.adapters.repositories.organization.organization_repository import OrganizationRepository
from app.use_cases.base_case import BaseUseCase


class AllClientOrganizationCase(BaseUseCase[list[OrganizationWithRelationsDTO]]):
    def __init__(self, db: AsyncSession):
        self.repository = OrganizationRepository(db)

    async def execute(
        self, filter: OrganizationClientFilter,
            client_id:int
    ) -> list[OrganizationWithRelationsDTO]:
        models = await self.repository.get_with_filters(
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            options=self.repository.default_relationships(),
            filters=filter.apply(client_id=client_id),
        )
        return [OrganizationWithRelationsDTO.from_orm(model) for model in models]

    async def validate(self):
        pass