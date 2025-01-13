from typing import Optional

from sqlalchemy import and_, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.kaspi.kaspi_payment_dto import KaspiPaymentCDTO
from app.adapters.dto.kaspi.kaspi_payment_pay_dto import (
    KaspiPaymentPayRequestDTO,
    KaspiPaymentPayResponseDTO,
)
from app.adapters.dto.order.order_dto import OrderCDTO
from app.adapters.repositories.kaspi_payment.kaspi_payment_repository import (
    KaspiPaymentRepository,
)
from app.adapters.repositories.order.order_repository import OrderRepository
from app.adapters.repositories.order_status.order_status_repository import (
    OrderStatusRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import KaspiPaymentModel, OrderModel
from app.infrastructure.helpers.kaspi_payment_helper import KaspiPaymentHelper
from app.shared.db_constants import AppDbValueConstants
from app.use_cases.base_case import BaseUseCase


class PayKaspiPaymentCase(BaseUseCase[KaspiPaymentPayResponseDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = KaspiPaymentRepository(db)
        self.order_repository = OrderRepository(db)
        self.order_status_repository = OrderStatusRepository(db)

    async def execute(
        self, dto: KaspiPaymentPayRequestDTO
    ) -> KaspiPaymentPayResponseDTO:
        order = await self._get_order(dto)
        kaspi_payment = await self._get_kaspi_payment(dto)

        if not order:
            return self._create_response(
                dto=dto, result=KaspiPaymentHelper.NOT_FOUND, comment="Заказ не найден"
            )

        if not kaspi_payment:
            return self._create_response(
                dto=dto, result=KaspiPaymentHelper.NOT_FOUND, comment="Платеж не найден"
            )

        if kaspi_payment and order.price_with_taxes == dto.sum:
            await self._process_payment(order, dto, kaspi_payment, success=True)
            return self._create_response(
                dto=dto,
                result=KaspiPaymentHelper.AVAILABLE_FOR_PAYMENT,
                comment="Оплата успешно произведена",
                sum=order.price_with_taxes,
                prv_txn_id=kaspi_payment.txn_check_id,
            )
        if order.price_with_taxes != dto.sum:
            return self._create_response(
                dto=dto,
                result=KaspiPaymentHelper.PROVIDER_ERROR,
                comment=f"Сумма недостаточно для оплаты заказа {order.price_with_taxes}, а вы оплачиваете {dto.sum}",
                sum=order.price_with_taxes,
            )

        await self._process_payment(order, dto, kaspi_payment, success=False)
        return self._create_response(
            dto=dto,
            result=KaspiPaymentHelper.PROVIDER_ERROR,
            comment="Что-то пошло не так",
            sum=order.price_with_taxes,
        )

    async def validate(self, dto: KaspiPaymentPayRequestDTO):
        return

    async def _get_order(self, dto: KaspiPaymentPayRequestDTO) -> Optional[OrderModel]:
        return await self.order_repository.get_first_with_filters(
            filters=[
                and_(
                    func.lower(self.order_repository.model.zakaz)
                    == dto.account.lower(),
                    self.order_repository.model.status.in_([
                        AppDbValueConstants.WAITING_FOR_PAYMENT_STATUS,
                        AppDbValueConstants.PAYMENT_REJECTED_STATUS
                    ])
                )
            ],
            options=self.order_repository.default_relationships(),
        )

    async def _get_kaspi_payment(
        self, dto: KaspiPaymentPayRequestDTO
    ) -> Optional[KaspiPaymentModel]:
        return await self.repository.get_first_with_filters(
            filters=[
                and_(
                    func.lower(self.repository.model.account) == dto.account.lower(),
                    func.lower(self.repository.model.command)
                    == KaspiPaymentHelper.CHECK_COMMAND.lower(),
                )
            ]
        )

    async def _process_payment(
        self,
        order: OrderModel,
        dto: KaspiPaymentPayRequestDTO,
        kaspi_payment: KaspiPaymentModel,
        success: bool,
    ):
        payment_dto = self._prepare_payment_dto(kaspi_payment, dto, success)
        updated_kaspi_payment = await self.repository.update(
            obj=kaspi_payment, dto=payment_dto
        )
        await self._update_order_status(order, updated_kaspi_payment, success)

    def _prepare_payment_dto(
        self,
        kaspi_payment: KaspiPaymentModel,
        dto: KaspiPaymentPayRequestDTO,
        success: bool,
    ) -> KaspiPaymentCDTO:
        payment_dto = KaspiPaymentCDTO.from_orm(kaspi_payment)
        payment_dto.txn_id = dto.txn_id
        payment_dto.txn_pay_id = dto.txn_id
        payment_dto.command = KaspiPaymentHelper.PAY_COMMAND
        if success:
            payment_dto.is_paid = True
            payment_dto.is_failed = False
            payment_dto.txn_date = dto.txn_date
            payment_dto.paid_at = KaspiPaymentHelper.get_paid_date_and_time(
                dto.txn_date
            )[2]
        else:
            payment_dto.is_paid = False
            payment_dto.is_failed = True
        return payment_dto

    async def _update_order_status(
        self, order: OrderModel, kaspi_payment: KaspiPaymentModel, success: bool
    ):
        status_value = (
            AppDbValueConstants.PAID_WAITING_FOR_BOOKING_STATUS.lower()
            if success
            else AppDbValueConstants.PAYMENT_REJECTED_STATUS.lower()
        )
        order_status = await self._get_order_status(status_value)
        dto = self._prepare_order_dto(order, kaspi_payment, order_status, success)
        await self.order_repository.update(obj=order, dto=dto)

    async def _get_order_status(self, status_value: str):
        order_status = await self.order_status_repository.get_first_with_filters(
            filters=[
                func.lower(self.order_status_repository.model.value) == status_value
            ]
        )
        if not order_status:
            raise AppExceptionResponse.internal_error("Статус заказа не найден")
        return order_status

    def _prepare_order_dto(
        self,
        order: OrderModel,
        kaspi_payment: KaspiPaymentModel,
        order_status,
        success: bool,
    ) -> OrderCDTO:
        dto = OrderCDTO.from_orm(order)
        if success:
            dto.kaspi_id = kaspi_payment.id
            dto.txn_id = kaspi_payment.txn_id
            dto.is_paid = True
            dto.paid_at = kaspi_payment.paid_at
        else:
            dto.kaspi_id = None
            dto.txn_id = None
            dto.is_paid = False
        dto.status_id = order_status.id
        dto.status = order_status.value
        return dto

    def _create_response(
        self,
        dto: KaspiPaymentPayRequestDTO,
        result: str,
        comment: str,
        sum: Optional[float] = None,
        prv_txn_id: Optional[str] = None,
    ) -> KaspiPaymentPayResponseDTO:
        return KaspiPaymentPayResponseDTO(
            txn_id=dto.txn_id,
            prv_txn_id=prv_txn_id or dto.txn_id,
            result=result,
            sum=sum or dto.sum,
            comment=comment,
        )
