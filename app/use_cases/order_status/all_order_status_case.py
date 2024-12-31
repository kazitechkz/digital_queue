from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.dto.order_status.order_status_dto import (
    OrderStatusRDTO, OrderStatusWithRelationsDTO)
from app.adapters.repositories.order_status.order_status_repository import \
    OrderStatusRepository
from app.use_cases.base_case import BaseUseCase


class AllOrderStatusCase(BaseUseCase[list[OrderStatusWithRelationsDTO]]):
    def __init__(self, db: AsyncSession):
        self.repository = OrderStatusRepository(db)

    async def execute(self) -> list[OrderStatusWithRelationsDTO]:
        models = await self.repository.get_all(
            options=[
                selectinload(self.repository.model.prev_order_status),
                selectinload(self.repository.model.next_order_status),
            ],
            order_by="id",
        )
        print(models)
        return [OrderStatusWithRelationsDTO.from_orm(model) for model in models]

    async def validate(self):
        pass
