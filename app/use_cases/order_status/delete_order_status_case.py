from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repositories.order_status.order_status_repository import \
    OrderStatusRepository
from app.core.app_exception_response import AppExceptionResponse
from app.shared.db_constants import AppDbValueConstants
from app.use_cases.base_case import BaseUseCase


class DeleteOrderStatusCase(BaseUseCase[bool]):
    def __init__(self, db: AsyncSession):
        self.repository = OrderStatusRepository(db)

    async def execute(self, id: int) -> bool:
        await self.validate(id=id)
        data = await self.repository.delete(id=id)
        return data

    async def validate(self, id: int):
        existed = await self.repository.get(id=id)
        if existed is None:
            raise AppExceptionResponse.not_found(message="Статус заказа не найден")
        if existed.value in AppDbValueConstants.IMMUTABLE_ORDER_STATUS:
            raise AppExceptionResponse.bad_request(
                message="Данный статус заказа нельзя удалять"
            )
