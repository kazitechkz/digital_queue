from typing import Optional

from sqlalchemy import and_, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.kaspi.kaspi_payment_dto import KaspiPaymentCDTO
from app.adapters.dto.kaspi.kaspi_payment_pay_dto import KaspiPaymentPayResponseDTO, KaspiPaymentPayRequestDTO
from app.adapters.dto.order.order_dto import OrderCDTO
from app.adapters.repositories.kaspi_payment.kaspi_payment_repository import KaspiPaymentRepository
from app.adapters.repositories.order.order_repository import OrderRepository
from app.adapters.repositories.order_status.order_status_repository import OrderStatusRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import OrderModel, KaspiPaymentModel
from app.infrastructure.helpers.kaspi_payment_helper import KaspiPaymentHelper
from app.shared.db_constants import AppDbValueConstants
from app.use_cases.base_case import BaseUseCase


class PayKaspiPaymentCase(BaseUseCase[KaspiPaymentPayResponseDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = KaspiPaymentRepository(db)
        self.order_repository = OrderRepository(db)
        self.order_status_repository = OrderStatusRepository(db)

    async def execute(self,dto:KaspiPaymentPayRequestDTO) -> KaspiPaymentPayResponseDTO:
        order = await self.order_repository.get_first_with_filters(
            filters=[and_(
                func.lower(self.order_repository.model.zakaz) == dto.account.lower(),
                func.lower(self.order_repository.model.status) == AppDbValueConstants.WAITING_FOR_PAYMENT_STATUS.lower(),
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
        return await self.transform(order, kaspi_payment, dto)

    async def validate(self):
        pass

    async def transform(self,order:Optional[OrderModel],kaspi_payment:Optional[KaspiPaymentModel],dto:KaspiPaymentPayRequestDTO):
        if not order:
            return KaspiPaymentPayResponseDTO(
                txn_id = dto.txn_id,
                prv_txn_id = dto.txn_id,
                result = KaspiPaymentHelper.NOT_FOUND,
                sum = dto.sum,
                comment = "Заказ не найден"
            )
        elif not kaspi_payment:
            return KaspiPaymentPayResponseDTO(
                txn_id=dto.txn_id,
                prv_txn_id=dto.txn_id,
                result=KaspiPaymentHelper.NOT_FOUND,
                sum=dto.sum,
                comment="Заказ не найден"
            )
        #Платежка проходит
        elif kaspi_payment and order.price_with_taxes == dto.sum:
            await self._create_kaspi_payment(order=order, dto=dto, kaspi_payment=kaspi_payment, success=True)
            return KaspiPaymentPayResponseDTO(
                txn_id=dto.txn_id,
                prv_txn_id=kaspi_payment.txn_check_id,
                result=KaspiPaymentHelper.AVAILABLE_FOR_PAYMENT,
                sum=order.price_with_taxes,
                comment="Оплата успешно произведена"
            )
        else:
            await self._create_kaspi_payment(order=order, dto=dto, kaspi_payment=kaspi_payment, success=False)
            return KaspiPaymentPayResponseDTO(
                txn_id=dto.txn_id,
                prv_txn_id=dto.txn_id,
                result=KaspiPaymentHelper.PROVIDER_ERROR,
                sum=order.price_with_taxes,
                comment="Что-то пошло не так"
            )

    async def _create_kaspi_payment(self,order:OrderModel,dto:KaspiPaymentPayRequestDTO,kaspi_payment:KaspiPaymentModel,success:bool):
        payment_dto = KaspiPaymentCDTO.from_orm(kaspi_payment)
        if success:
            payment_dto.txn_id = dto.txn_id
            payment_dto.command = KaspiPaymentHelper.PAY_COMMAND
            payment_dto.is_paid = True
            payment_dto.is_failed = False
            payment_dto.paid_at = KaspiPaymentHelper.get_paid_date_and_time(dto.txn_date)[2]
        else:
            payment_dto.txn_id = dto.txn_id
            payment_dto.command = KaspiPaymentHelper.PAY_COMMAND
            payment_dto.is_failed = True
            payment_dto.is_paid = False
        update_kaspi_payment = await self.repository.update(obj=kaspi_payment,dto=payment_dto)
        await self._update_order_status(order=order,kaspi_payment=update_kaspi_payment,success=success)


    async def _update_order_status(self, order,kaspi_payment:KaspiPaymentModel,success:bool):
        dto = OrderCDTO.from_orm(order)
        if success:
            order_status = await self.order_status_repository.get_first_with_filters(
                filters=[func.lower(
                    self.order_status_repository.model.value) == AppDbValueConstants.PAID_WAITING_FOR_BOOKING_STATUS.lower()]
            )
            if not order_status:
                raise AppExceptionResponse.internal_error("Статус заказа не найден")
            dto.kaspi_id = kaspi_payment.id
            dto.txn_id = kaspi_payment.txn_id
            dto.is_paid = True
            dto.paid_at = kaspi_payment.paid_at
            dto.status = order_status.value
            dto.status_id = order_status.id
        else:
            order_status = await self.order_status_repository.get_first_with_filters(
                filters=[func.lower(
                    self.order_status_repository.model.value) == AppDbValueConstants.PAYMENT_REJECTED_STATUS.lower()]
            )
            if not order_status:
                raise AppExceptionResponse.internal_error("Статус заказа не найден")
            dto.is_paid = False
            dto.kaspi_id = None
            dto.txn_id = None
            dto.status = order_status.value
            dto.status_id = order_status.id
        await self.order_repository.update(obj=order,dto=dto)