from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.organization_employee.organization_employee_dto import (
    OrganizationEmployeeWithRelationsDTO,
)
from app.adapters.dto.pagination_dto import (
    PaginationOrganizationEmployeeWithRelationsDTO,
)
from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.adapters.filters.organization_employee.client.organization_employee_client_filter import (
    OrganizationEmployeeClientFilter,
)
from app.adapters.repositories.organization_employee.organization_employee_repository import (
    OrganizationEmployeeRepository,
)
from app.use_cases.base_case import BaseUseCase


class AllClientOrganizationEmployeeCase(
    BaseUseCase[list[OrganizationEmployeeWithRelationsDTO]]
):
    def __init__(self, db: AsyncSession):
        self.repository = OrganizationEmployeeRepository(db)

    async def execute(
        self, filter: OrganizationEmployeeClientFilter, user: UserWithRelationsDTO
    ) -> list[OrganizationEmployeeWithRelationsDTO]:
        models = await self.repository.get_with_filters(
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            options=self.repository.default_relationships(),
            filters=filter.apply(user=user),
        )
        return [
            OrganizationEmployeeWithRelationsDTO.from_orm(model) for model in models
        ]

    async def validate(self):
        pass
