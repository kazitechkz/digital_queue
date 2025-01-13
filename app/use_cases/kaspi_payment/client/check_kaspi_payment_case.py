from typing import Optional

from sqlalchemy import and_, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.kaspi.kaspi_payment_check_dto import (
    KaspiPaymentCheckRequestDTO,
    KaspiPaymentCheckResponseDTO,
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


class CheckKaspiPaymentCase(BaseUseCase[KaspiPaymentCheckResponseDTO]):
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = KaspiPaymentRepository(db)
        self.order_repository = OrderRepository(db)
        self.order_status_repository = OrderStatusRepository(db)

    async def execute(
        self, dto: KaspiPaymentCheckRequestDTO
    ) -> KaspiPaymentCheckResponseDTO:
        order = await self._get_order(dto)
        kaspi_payment = await self._get_kaspi_payment(dto)
        return await self._generate_response(order, kaspi_payment, dto)

    async def _get_order(
        self, dto: KaspiPaymentCheckRequestDTO
    ) -> Optional[OrderModel]:
        return await self.order_repository.get_first_with_filters(
            filters=[
                and_(
                    func.lower(self.order_repository.model.zakaz)
                    == dto.account.lower(),
                    or_(
                        func.lower(self.order_repository.model.status)
                        == AppDbValueConstants.WAITING_FOR_PAYMENT_STATUS.lower(),
                        func.lower(self.order_repository.model.status)
                        == AppDbValueConstants.PAYMENT_REJECTED_STATUS.lower(),
                    ),
                )
            ],
            options=self.order_repository.default_relationships(),
        )

    async def _get_kaspi_payment(
        self, dto: KaspiPaymentCheckRequestDTO
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

    async def _generate_response(
        self,
        order: Optional[OrderModel],
        kaspi_payment: Optional[KaspiPaymentModel],
        dto: KaspiPaymentCheckRequestDTO,
    ) -> KaspiPaymentCheckResponseDTO:
        if not order:
            return self._order_not_found_response(dto)
        if not kaspi_payment and not order.is_paid:
            kaspi_payment = await self._create_kaspi_payment(order, dto)
            return self._success_response(kaspi_payment, order)
        if order.is_paid:
            return self._already_paid_response(dto, order)
        if kaspi_payment and not order.is_paid:
            return await self._handle_existing_kaspi_payment(kaspi_payment, order, dto)
        return self._provider_error_response(dto, order)

    async def _create_kaspi_payment(
        self, order: OrderModel, dto: KaspiPaymentCheckRequestDTO
    ) -> KaspiPaymentModel:
        if order.status == AppDbValueConstants.PAYMENT_REJECTED_STATUS:
            await self._update_order_status(order)
        return await self.repository.create(
            obj=KaspiPaymentModel(
                order_id=order.id,
                zakaz=order.zakaz,
                account=order.zakaz,
                txn_id=dto.txn_id,
                txn_check_id=dto.txn_id,
                command=KaspiPaymentHelper.CHECK_COMMAND,
                sum=order.price_with_taxes,
                amount=order.quan_t,
                is_failed=False,
                is_paid=False,
                is_qr_generate=False,
            )
        )

    async def _update_order_status(self, order: OrderModel):
        order_status = await self.order_status_repository.get_first_with_filters(
            filters=[
                func.lower(self.order_status_repository.model.value)
                == AppDbValueConstants.WAITING_FOR_PAYMENT_STATUS.lower()
            ]
        )
        if not order_status:
            raise AppExceptionResponse.internal_error(
                "Статус ожидания платежа не найден"
            )
        dto = OrderCDTO.from_orm(order)
        dto.status_id = order_status.id
        dto.status = AppDbValueConstants.WAITING_FOR_PAYMENT_STATUS
        await self.order_repository.update(obj=order, dto=dto)

    async def _handle_existing_kaspi_payment(
        self,
        kaspi_payment: KaspiPaymentModel,
        order: OrderModel,
        dto: KaspiPaymentCheckRequestDTO,
    ) -> KaspiPaymentCheckResponseDTO:
        if kaspi_payment.txn_id != dto.txn_id:
            await self.repository.delete(id=kaspi_payment.id)
            kaspi_payment = await self._create_kaspi_payment(order, dto)
        return self._success_response(kaspi_payment, order)

    def _order_not_found_response(
        self, dto: KaspiPaymentCheckRequestDTO
    ) -> KaspiPaymentCheckResponseDTO:
        return KaspiPaymentCheckResponseDTO(
            txn_id=dto.txn_id,
            result=KaspiPaymentHelper.NOT_FOUND,
            sum=0,
            comment="Заказ не найден",
        )

    def _already_paid_response(
        self, dto: KaspiPaymentCheckRequestDTO, order: OrderModel
    ) -> KaspiPaymentCheckResponseDTO:
        return KaspiPaymentCheckResponseDTO(
            txn_id=dto.txn_id,
            result=KaspiPaymentHelper.ALREADY_PAID,
            sum=order.price_with_taxes,
            comment="Вы уже оплатили данный заказ",
        )

    def _provider_error_response(
        self, dto: KaspiPaymentCheckRequestDTO, order: OrderModel
    ) -> KaspiPaymentCheckResponseDTO:
        return KaspiPaymentCheckResponseDTO(
            txn_id=dto.txn_id,
            result=KaspiPaymentHelper.PROVIDER_ERROR,
            sum=order.price_with_taxes,
            comment="Что-то пошло не так",
        )

    def _success_response(
        self, kaspi_payment: KaspiPaymentModel, order: OrderModel
    ) -> KaspiPaymentCheckResponseDTO:
        return KaspiPaymentCheckResponseDTO(
            txn_id=kaspi_payment.txn_check_id,
            result=KaspiPaymentHelper.AVAILABLE_FOR_PAYMENT,
            sum=order.price_with_taxes,
            comment="Заказ готов к оплате",
            fields={
                "field1": {"@name": "Покупатель", "#text": f"{order.name}"},
                "field2": {"@name": "Товар", "#text": f"{order.material.title}"},
                "field3": {"@name": "Кол-во", "#text": f"{order.quan_t} тонн"},
                "field4": {
                    "@name": "Идентификатор покупателя (БИН или ИИН)",
                    "#text": f"{order.bin or order.iin}",
                },
            },
        )
