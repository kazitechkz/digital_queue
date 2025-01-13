from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.employee_request.employee_request_dto import (
    EmployeeRequestWithRelationsDTO,
)
from app.adapters.dto.pagination_dto import PaginationEmployeeRequestWithRelationsDTO
from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.adapters.filters.employee_request.client.employee_request_client_filter import (
    EmployeeRequestClientFilter,
)
from app.adapters.repositories.employee_request.employee_request_repository import (
    EmployeeRequestRepository,
)
from app.use_cases.base_case import BaseUseCase


class PaginateEmployeeRequestCase(
    BaseUseCase[PaginationEmployeeRequestWithRelationsDTO]
):
    def __init__(self, db: AsyncSession):
        self.repository = EmployeeRequestRepository(db)

    async def execute(
        self, filter: EmployeeRequestClientFilter, user: UserWithRelationsDTO
    ) -> PaginationEmployeeRequestWithRelationsDTO:
        models = await self.repository.paginate(
            dto=EmployeeRequestWithRelationsDTO,
            page=filter.page,
            per_page=filter.per_page,
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            options=self.repository.default_relationships(),
            filters=filter.apply(user),
        )
        return models

    async def validate(self):
        pass
