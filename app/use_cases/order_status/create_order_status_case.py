from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.dto.order_status.order_status_dto import (
    OrderStatusCDTO,
    OrderStatusWithRelationsDTO,
)
from app.adapters.repositories.order_status.order_status_repository import (
    OrderStatusRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class CreateOrderStatusCase(BaseUseCase[OrderStatusWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = OrderStatusRepository(db)

    async def execute(self, dto: OrderStatusCDTO) -> OrderStatusWithRelationsDTO:
        obj = await self.validate(dto=dto)
        data = await self.repository.create(obj=obj)
        if not data:
            raise AppExceptionResponse.not_found("Статус заказа не найден")
        else:
            existed = await self.repository.get(
                id=data.id,
                options=self.repository.default_relationships(),
            )
        return OrderStatusWithRelationsDTO.from_orm(existed)

    async def validate(self, dto: OrderStatusCDTO):
        dict_dto = dto.dict()
        existed = await self.repository.get_first_with_filters(
            filters=[func.lower(self.repository.model.value) == dto.value.lower()]
        )
        if existed:
            raise AppExceptionResponse.bad_request(
                "Статус заказа с таким значением уже существует"
            )
        if dto.next_id:
            next_obj = await self.repository.get(id=dto.next_id)
            if not next_obj:
                raise AppExceptionResponse.bad_request("Следующий статус не найден")
            else:
                dict_dto["next_value"] = next_obj.value
        if dto.prev_id:
            prev_obj = await self.repository.get(id=dto.prev_id)
            if not prev_obj:
                raise AppExceptionResponse.bad_request("Предыдущий статус не найден")
            else:
                dict_dto["prev_value"] = prev_obj.value

        return self.repository.model(**dict_dto)
