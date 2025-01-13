from typing import Any, Optional

from sqlalchemy import and_, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.kaspi.kaspi_request_dto import (
    KaspiFastPaymentDTO,
    KaspiFastPaymentFrontendRequestDTO,
    KaspiFastPaymentResponseDTO,
)
from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.adapters.repositories.kaspi_payment.kaspi_payment_repository import (
    KaspiPaymentRepository,
)
from app.adapters.repositories.order.order_repository import OrderRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import OrderModel
from app.infrastructure.api_clients.kaspi.kaspi_api_client import KaspiPaymentApiClient
from app.infrastructure.config import app_config
from app.infrastructure.helpers.kaspi_payment_helper import KaspiPaymentHelper
from app.shared.db_constants import AppDbValueConstants
from app.use_cases.base_case import BaseUseCase


class CreateFastPaymentCase(BaseUseCase[KaspiFastPaymentResponseDTO]):
    def __init__(self, db: AsyncSession):
        self.order_repository = OrderRepository(db)
        self.service = KaspiPaymentApiClient()

    async def execute(
        self, dto: KaspiFastPaymentFrontendRequestDTO, user: UserWithRelationsDTO
    ) -> KaspiFastPaymentResponseDTO:
        order = await self.order_repository.get_first_with_filters(
            filters=[
                and_(
                    self.order_repository.model.id == dto.order_id,
                    or_(
                        self.order_repository.model.owner_id == user.id,
                        self.order_repository.model.iin == user.iin,
                        self.order_repository.model.owner_sid == user.sid,
                    ),
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
        await self.validate(order=order)
        kaspi_request_dto: KaspiFastPaymentDTO = await self.transform(
            dto=dto, order=order
        )
        return await self.service.fast_payments(dto=kaspi_request_dto)

    async def validate(self, order: Optional[OrderModel]):
        if not order:
            raise AppExceptionResponse.bad_request("Заказ не найден или уже оплачен")

    async def transform(
        self, dto: KaspiFastPaymentFrontendRequestDTO, order: OrderModel
    ) -> KaspiFastPaymentDTO:
        return KaspiFastPaymentDTO(
            TranId=str(order.id),
            OrderId=order.zakaz,
            Amount=KaspiPaymentHelper.convert_to_tiin(price=order.price_with_taxes),
            Service=app_config.fast_payment_kaspi_service,
            returnUrl=f"{app_config.fast_payment_kaspi_return_url}?order_id={order.id}",
            refererHost=app_config.fast_payment_kaspi_refer_host,
            GenerateQrCode=dto.generate_qr_code,
        )
