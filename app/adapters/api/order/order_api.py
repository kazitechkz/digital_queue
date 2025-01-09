from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.order.create_order_dto import CreateOrderDTO
from app.adapters.dto.order.order_dto import OrderWithRelationsDTO
from app.adapters.dto.order_status.order_status_dto import OrderStatusWithRelationsDTO
from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.core.api_middleware_core import check_client
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.database import get_db
from app.shared.path_constants import AppPathConstants
from app.use_cases.order.client.create_order_case import CreateClientOrderCase


class OrderApi:

    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.post(
            f"{AppPathConstants.CreateClientOrderRequestPathName}",
            response_model=OrderWithRelationsDTO,
            summary="Создать статус заказа клиента",
            description="Создание статуса заказа клиента",
        )(self.create_client_order)


    async def create_client_order(self,
                            dto:CreateOrderDTO,
                            user:UserWithRelationsDTO = Depends(check_client),
                            db: AsyncSession = Depends(get_db)
                            ):
        use_case = CreateClientOrderCase(db)
        try:
            return await use_case.execute(dto=dto,user=user)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании заказа",
                extra={"details": f"{str(exc)}"},
                is_custom=True,
            )