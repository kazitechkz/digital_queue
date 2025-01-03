from sqlalchemy import and_, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.dto.order_status.order_status_dto import \
    OrderStatusWithRelationsDTO
from app.adapters.repositories.order_status.order_status_repository import \
    OrderStatusRepository
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class GetOrderStatusByValueCase(BaseUseCase[OrderStatusWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = OrderStatusRepository(db)

    async def execute(self, value: str) -> OrderStatusWithRelationsDTO:
        filters = [
            and_(
                func.lower(self.repository.model.value) == value.lower(),
            )
        ]
        model = await self.repository.get_first_with_filters(
            filters=filters,
            options=self.repository.default_relationships(),
        )
        if not model:
            raise AppExceptionResponse.not_found("Статус Заказа не найден")
        return OrderStatusWithRelationsDTO.from_orm(model)

    async def validate(self):
        pass
