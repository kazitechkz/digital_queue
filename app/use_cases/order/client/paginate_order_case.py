from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.order.order_dto import OrderWithRelationsDTO
from app.adapters.dto.pagination_dto import PaginationOrderWithRelationsDTO
from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.adapters.filters.order.client.order_client_filter import OrderClientFilter
from app.adapters.repositories.order.order_repository import OrderRepository
from app.use_cases.base_case import BaseUseCase


class PaginateClientOrderCase(BaseUseCase[PaginationOrderWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = OrderRepository(db)

    async def execute(
        self, filter: OrderClientFilter,user:UserWithRelationsDTO
    ) -> PaginationOrderWithRelationsDTO:
        models = await self.repository.paginate(
            dto=OrderWithRelationsDTO,
            page=filter.page,
            per_page=filter.per_page,
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            options=self.repository.default_relationships(),
            filters=filter.apply(user=user),
        )
        return models

    async def validate(self):
        pass
