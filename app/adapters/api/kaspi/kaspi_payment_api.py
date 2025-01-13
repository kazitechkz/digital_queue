from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.kaspi.kaspi_payment_check_dto import (
    KaspiPaymentCheckRequestDTO,
    KaspiPaymentCheckResponseDTO,
)
from app.adapters.dto.kaspi.kaspi_payment_pay_dto import (
    KaspiPaymentPayRequestDTO,
    KaspiPaymentPayResponseDTO,
)
from app.adapters.dto.kaspi.kaspi_request_dto import (
    KaspiFastPaymentFrontendRequestDTO,
    KaspiFastPaymentResponseDTO,
)
from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.core.api_middleware_core import check_client
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.database import get_db
from app.shared.path_constants import AppPathConstants
from app.use_cases.kaspi_payment.client.check_kaspi_payment_case import (
    CheckKaspiPaymentCase,
)
from app.use_cases.kaspi_payment.client.create_fast_payment_case import (
    CreateFastPaymentCase,
)
from app.use_cases.kaspi_payment.client.pay_kaspi_payment_case import (
    PayKaspiPaymentCase,
)


class KaspiPaymentApi:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            f"{AppPathConstants.KaspiCheckPathName}",
            response_model=KaspiPaymentCheckResponseDTO,
            summary="Сервис каспи для проверки заказа",
            description="Проверка каспи для заказа (Check)",
        )(self.check)
        self.router.get(
            f"{AppPathConstants.KaspiPayPathName}",
            response_model=KaspiPaymentPayResponseDTO,
            summary="Сервис каспи для проверки заказа",
            description="Проверка каспи для заказа (Check)",
        )(self.pay)
        self.router.post(
            f"{AppPathConstants.KaspiFastPaymentPathName}",
            response_model=KaspiFastPaymentResponseDTO,
            summary="Сервис каспи для генерации URL ссылки",
            description="Генерация ссылки для оплаты и QR-код",
        )(self.fast_payment)

    async def check(
        self,
        dto: KaspiPaymentCheckRequestDTO = Depends(),
        db: AsyncSession = Depends(get_db),
    ):
        use_case = CheckKaspiPaymentCase(db)
        try:
            return await use_case.execute(dto=dto)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при проверке заказа",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def pay(
        self,
        dto: KaspiPaymentPayRequestDTO = Depends(),
        db: AsyncSession = Depends(get_db),
    ):
        use_case = PayKaspiPaymentCase(db)
        try:
            return await use_case.execute(dto=dto)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при оплате заказа",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def fast_payment(
        self,
        dto: KaspiFastPaymentFrontendRequestDTO = Depends(),
        user: UserWithRelationsDTO = Depends(check_client),
        db: AsyncSession = Depends(get_db),
    ):
        use_case = CreateFastPaymentCase(db)
        try:
            return await use_case.execute(dto=dto, user=user)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при оплате заказа",
                extra={"details": str(exc)},
                is_custom=True,
            )
