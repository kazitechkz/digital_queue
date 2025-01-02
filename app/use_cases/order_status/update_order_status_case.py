from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.dto.order_status.order_status_dto import (
    OrderStatusCDTO,
    OrderStatusRDTO,
    OrderStatusWithRelationsDTO,
)
from app.adapters.repositories.order_status.order_status_repository import (
    OrderStatusRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class UpdateOrderStatusCase(BaseUseCase[OrderStatusWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = OrderStatusRepository(db)

    async def execute(
        self, id: int, dto: OrderStatusCDTO
    ) -> OrderStatusWithRelationsDTO:
        obj = await self.validate(id=id, dto=dto)
        data = await self.repository.update(obj=obj, dto=dto)
        if not data:
            raise AppExceptionResponse.not_found("Статус заказа не найден")
        else:
            existed = await self.repository.get(
                id=data.id,
                options=[
                    selectinload(self.repository.model.prev_order_status),
                    selectinload(self.repository.model.next_order_status),
                ],
            )
        return OrderStatusWithRelationsDTO.from_orm(existed)

    async def validate(self, id: int, dto: OrderStatusCDTO):
        existed = await self.repository.get(id=id)
        if existed is None:
            raise AppExceptionResponse.not_found(message="Статус заказа не найден")
        if await self.repository.get_first_with_filters(
            [
                func.lower(self.repository.model.value) == dto.value.lower(),
                self.repository.model.id != id,
            ]
        ):
            raise AppExceptionResponse.bad_request(
                "Статус заказа с таким значением уже существует"
            )
        if dto.next_id:
            next_obj = await self.repository.get(id=dto.next_id)
            if not next_obj:
                raise AppExceptionResponse.bad_request("Следующий статус не найден")
            elif next_obj.value != dto.next_value:
                raise AppExceptionResponse.bad_request(
                    "Данные следующего статуса не совпадает"
                )
        if dto.prev_id:
            prev_obj = await self.repository.get(id=dto.prev_id)
            if not prev_obj:
                raise AppExceptionResponse.bad_request("Предыдущий статус не найден")
            elif prev_obj.value != dto.prev_value:
                raise AppExceptionResponse.bad_request(
                    "Данные предыдущего статуса не совпадает"
                )
        return existed
