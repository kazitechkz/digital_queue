from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.dto.order_status.order_status_dto import OrderStatusWithRelationsDTO
from app.adapters.repositories.order_status.order_status_repository import (
    OrderStatusRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class GetOrderStatusByIdCase(BaseUseCase[OrderStatusWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = OrderStatusRepository(db)

    async def execute(self, id: int) -> OrderStatusWithRelationsDTO:
        model = await self.repository.get(
            id,
            options=self.repository.default_relationships(),
        )
        if not model:
            raise AppExceptionResponse.not_found("Статус заказа не найден")
        return OrderStatusWithRelationsDTO.from_orm(model)

    async def validate(self):
        pass
