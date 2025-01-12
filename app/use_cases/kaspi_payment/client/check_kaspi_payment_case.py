from typing import Optional

from sqlalchemy import and_, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.kaspi.kaspi_payment_check_dto import KaspiPaymentCheckRequestDTO, KaspiPaymentCheckResponseDTO
from app.adapters.dto.order.order_dto import OrderCDTO
from app.adapters.repositories.kaspi_payment.kaspi_payment_repository import KaspiPaymentRepository
from app.adapters.repositories.order.order_repository import OrderRepository
from app.adapters.repositories.order_status.order_status_repository import OrderStatusRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import OrderModel, KaspiPaymentModel
from app.infrastructure.helpers.kaspi_payment_helper import KaspiPaymentHelper
from app.shared.db_constants import AppDbValueConstants
from app.use_cases.base_case import BaseUseCase


class CheckKaspiPaymentCase(BaseUseCase[KaspiPaymentCheckResponseDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = KaspiPaymentRepository(db)
        self.order_repository = OrderRepository(db)
        self.order_status_repository = OrderStatusRepository(db)

    async def execute(self,dto:KaspiPaymentCheckRequestDTO) -> KaspiPaymentCheckResponseDTO:
        order = await self.order_repository.get_first_with_filters(
            filters=[and_(
                func.lower(self.order_repository.model.zakaz) == dto.account.lower(),
                or_(
                    func.lower(self.order_repository.model.status) == AppDbValueConstants.WAITING_FOR_PAYMENT_STATUS.lower(),
                    func.lower(self.order_repository.model.status) == AppDbValueConstants.PAYMENT_REJECTED_STATUS.lower(),
                )
            )],
            options=self.order_repository.default_relationships(),
        )
        kaspi_payment = await self.repository.get_first_with_filters(
            filters=[
                and_(
                    func.lower(self.repository.model.account) == dto.account.lower(),
                    func.lower(self.repository.model.command) == KaspiPaymentHelper.CHECK_COMMAND.lower(),
                )
            ]
        )
        dto = await self.transform(order=order,kaspi_payment=kaspi_payment,dto=dto)
        return dto


    async def validate(self):
        pass

    async def transform(self,order:Optional[OrderModel],kaspi_payment:Optional[KaspiPaymentModel],dto:KaspiPaymentCheckRequestDTO):
        if not order:
            return KaspiPaymentCheckResponseDTO(
                txn_id = dto.txn_id,
                result = KaspiPaymentHelper.NOT_FOUND,
                sum = 0,
                comment = "Заказ не найден"
            )
        elif not kaspi_payment and order.is_paid == False:
            kaspi_payment = await self._create_kaspi_payment(order, dto)
            return self._success_response(kaspi_payment=kaspi_payment, order=order)
        elif order.is_paid:
            return KaspiPaymentCheckResponseDTO(
                txn_id = dto.txn_id,
                result = KaspiPaymentHelper.ALREADY_PAID,
                sum = order.price_with_taxes,
                comment = "Вы уже оплатили данный заказ"
            )
        elif kaspi_payment.command.lower() == KaspiPaymentHelper.CHECK_COMMAND.lower() and kaspi_payment.txn_id != dto.txn_id and order.is_paid == False:
            await self.repository.delete(id=kaspi_payment.id)
            kaspi_payment = await self._create_kaspi_payment(order, dto)
            return self._success_response(kaspi_payment=kaspi_payment,order=order)
        elif kaspi_payment.command.lower() == KaspiPaymentHelper.CHECK_COMMAND.lower() and kaspi_payment.txn_id == dto.txn_id and order.is_paid == False:
            return self._success_response(kaspi_payment=kaspi_payment, order=order)
        else:
            return KaspiPaymentCheckResponseDTO(
                txn_id=dto.txn_id,
                result=KaspiPaymentHelper.PROVIDER_ERROR,
                sum=order.price_with_taxes,
                comment="Что-то пошло не так"
            )


    async def _create_kaspi_payment(self,order,dto):
        if order.status == AppDbValueConstants.PAYMENT_REJECTED_STATUS:
            await self._update_order_status(order)
        kaspi_payment = await self.repository.create(obj=KaspiPaymentModel(
            order_id=order.id,
            zakaz=order.zakaz,
            account=order.zakaz,
            txn_id=dto.txn_id,
            txn_check_id=dto.txn_id,
            txn_pay_id=None,
            txn_date=None,
            command=KaspiPaymentHelper.CHECK_COMMAND,
            sum=order.price_with_taxes,
            amount=order.quan_t,
            is_failed=False,
            is_paid=False,
            is_qr_generate=False,
            paid_at=None
        ))
        return kaspi_payment

    async def _update_order_status(self, order):
        dto = OrderCDTO.from_orm(order)
        order_status = await self.order_status_repository.get_first_with_filters(
            filters=[func.lower(self.order_status_repository.model.value) == AppDbValueConstants.WAITING_FOR_PAYMENT_STATUS.lower()]
        )
        if not order_status:
            raise AppExceptionResponse.internal_error("Статус ожидания платежа не найден")
        dto.status_id = order_status.id
        dto.status = AppDbValueConstants.WAITING_FOR_PAYMENT_STATUS
        await self.order_repository.update(obj=order,dto=dto)


    def _success_response(self,kaspi_payment,order):
        return KaspiPaymentCheckResponseDTO(
            txn_id=kaspi_payment.txn_check_id,
            result=KaspiPaymentHelper.AVAILABLE_FOR_PAYMENT,
            sum=order.price_with_taxes,
            comment="Заказ готов к оплате",
            fields={
                "field1": {
                    "@name": "Покупатель",
                    "#text": f"{order.name}"
                },
                "field2": {
                    "@name": "Товар",
                    "#text": f"{order.material.title}"
                },
                "field3": {
                    "@name": "Кол-во",
                    "#text": f"{order.quan_t} тонн"
                },
                "field4": {
                    "@name": "Идентификатор покупателя (БИН или ИИН)",
                    "#text": f"{order.bin or order.iin}"
                },
            }
        )