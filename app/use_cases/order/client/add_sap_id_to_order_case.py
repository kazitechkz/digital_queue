from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.adapters.dto.order.order_dto import OrderWithRelationsDTO, OrderCDTO
from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.adapters.repositories.order.order_repository import OrderRepository
from app.adapters.repositories.order_status.order_status_repository import OrderStatusRepository
from app.adapters.repositories.sap_request.sap_request_repository import SapRequestRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import SapRequestModel, OrderModel
from app.shared.db_constants import AppDbValueConstants
from app.use_cases.base_case import BaseUseCase


class AddSapIdToOrderCase(BaseUseCase[OrderWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = OrderRepository(db)
        self.order_status_repository = OrderStatusRepository(db)
        self.sap_request_repository = SapRequestRepository(db)

    async def execute(self,
                      sap_id: int,
                      user:UserWithRelationsDTO,
                      ) -> OrderWithRelationsDTO:
       sap_request = await self.sap_request_repository.get(id=sap_id)
       if not sap_request:
           raise AppExceptionResponse.bad_request("Заказ не найден")
       order = await self.repository.get(id=sap_request.order_id)
       if not order:
           raise AppExceptionResponse.bad_request("Заказ не найден")
       await self.validate(order=order, sap_request=sap_request, user=user)
       dto = await self.transform(order=order,sap_request=sap_request)
       model = await self.repository.update(obj = order, dto=dto)
       if not model:
        raise AppExceptionResponse.internal_error(message="Произошла ошибка при добавлении SAP-идентификатора")
       model = await self.repository.get(id=model.id,options=self.repository.default_relationships())
       return OrderWithRelationsDTO.from_orm(model)

    async def validate(self, order: OrderModel,sap_request:SapRequestModel,user:UserWithRelationsDTO):
        if order.sap_id or order.zakaz:
            raise AppExceptionResponse.bad_request(message="Заказ уже сформирован")
        if order.owner_id != user.id:
            raise AppExceptionResponse.bad_request(message="Заказ принадлежит не вам!")
        if order.status not in [AppDbValueConstants.WAITING_FOR_INVOICE_CREATION_STATUS, AppDbValueConstants.INVOICE_CREATION_ERROR_STATUS]:
            raise AppExceptionResponse.bad_request(message="Заказ находится на другом этапе")

    async def transform(self, order: OrderModel,sap_request:SapRequestModel)->OrderCDTO:
        dto = OrderCDTO.from_orm(order)
        if sap_request.is_active and sap_request.zakaz:
            next_status = await self.order_status_repository.get_first_with_filters(
                filters=[and_(self.order_status_repository.model.value == AppDbValueConstants.WAITING_FOR_PAYMENT_STATUS)]
            )
            if not next_status:
                raise AppExceptionResponse.bad_request(message="Статус не подходит для формирования счета")
            dto.zakaz = sap_request.zakaz
            dto.sap_id = sap_request.id
            dto.status_id = next_status.id
            dto.status = next_status.value
        else:
            if dto.status == AppDbValueConstants.WAITING_FOR_INVOICE_CREATION_STATUS:
                error_status = await self.order_status_repository.get_first_with_filters(
                    filters=[and_(
                        self.order_status_repository.model.value == AppDbValueConstants.INVOICE_CREATION_ERROR_STATUS)]
                )
                if not error_status:
                    raise AppExceptionResponse.bad_request(message="Статус не найден")
                dto.status_id = error_status.id
                dto.status = error_status.value

        return dto