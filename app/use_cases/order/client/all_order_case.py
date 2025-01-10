from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.order.order_dto import OrderWithRelationsDTO
from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.adapters.filters.order.client.order_client_filter import OrderClientFilter
from app.adapters.repositories.order.order_repository import OrderRepository
from app.use_cases.base_case import BaseUseCase


class AllClientOrderCase(BaseUseCase[list[OrderWithRelationsDTO]]):
    def __init__(self, db: AsyncSession):
        self.repository = OrderRepository(db)

    async def execute(self,parameters:OrderClientFilter,user:UserWithRelationsDTO) -> list[OrderWithRelationsDTO]:
        models = await self.repository.get_with_filters(
            options=self.repository.default_relationships(),
            filters=parameters.apply(user=user)
        )
        return [OrderWithRelationsDTO.from_orm(model) for model in models]

    async def validate(self):
        pass
