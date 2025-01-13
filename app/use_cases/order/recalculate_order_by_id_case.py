from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.order.order_dto import OrderWithRelationsDTO, OrderCDTO
from app.adapters.repositories.order.order_repository import OrderRepository
from app.core.app_exception_response import AppExceptionResponse
from app.shared.db_constants import AppDbValueConstants
from app.use_cases.base_case import BaseUseCase


class RecalculateOrderByIdCase(BaseUseCase[OrderWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = OrderRepository(db)

    async def execute(self,id:int) -> OrderWithRelationsDTO:
        order = await self.repository.get_first_with_filters(
            filters=[
                and_(
                    self.repository.model.id == id,
                    self.repository.model.status.in_([
                        AppDbValueConstants.PAID_WAITING_FOR_BOOKING_STATUS,
                        AppDbValueConstants.IN_PROGRESS_STATUS,
                    ])
                )
            ],
            options=self.repository.default_relationships()
        )
        if not order:
            raise AppExceptionResponse.bad_request("Заказ не найден")
        if order.schedules:
            quan_booked = 0
            quan_released = 0
            for schedule in order.schedules:
                #Count booked
                if schedule.is_active and not schedule.is_canceled and not schedule.is_executed:
                    quan_booked += schedule.loading_volume_kg
                if not schedule.is_active and not schedule.is_canceled and schedule.is_executed:
                    quan_released += schedule.vehicle_netto_kg

            cdto = OrderCDTO.from_orm(order)
            cdto.quan_booked = quan_booked
            cdto.quan_released = quan_released
            await self.repository.update(obj=order,dto=cdto)
            order = await self.repository.get(
                id=id,
                options=self.repository.default_relationships()
            )
        return OrderWithRelationsDTO.from_orm(order)


    async def validate(self):
        pass