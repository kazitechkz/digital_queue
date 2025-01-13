import traceback

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.order.create_order_dto import CreateOrderDTO
from app.adapters.dto.order.order_dto import OrderWithRelationsDTO
from app.adapters.dto.order_status.order_status_dto import OrderStatusWithRelationsDTO
from app.adapters.dto.pagination_dto import PaginationOrderWithRelationsDTO
from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.adapters.filters.order.client.order_client_filter import OrderClientFilter
from app.core.api_middleware_core import check_client
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.config import app_config
from app.infrastructure.database import get_db
from app.shared.path_constants import AppPathConstants
from app.use_cases.order.client.add_sap_id_to_order_case import AddSapIdToOrderCase
from app.use_cases.order.client.all_order_case import AllClientOrderCase
from app.use_cases.order.client.create_order_case import CreateClientOrderCase
from app.use_cases.order.client.get_order_by_id_case import GetClientOrderByIdCase
from app.use_cases.order.client.get_order_by_value_case import GetClientOrderByValueCase
from app.use_cases.order.client.paginate_order_case import PaginateClientOrderCase
from app.use_cases.sap.client.create_client_sap_order_case import (
    CreateClientSapOrderCase,
)


class OrderApi:

    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        # Client
        self.router.post(
            f"{AppPathConstants.CreateClientOrderRequestPathName}",
            response_model=OrderWithRelationsDTO,
            summary="Создать статус заказа клиента",
            description="Создание статуса заказа клиента",
        )(self.create_client_order)
        self.router.get(
            f"{AppPathConstants.AllClientOrderPathName}",
            response_model=list[OrderWithRelationsDTO],
            summary="Получить список заказов клиента",
            description="Получение списка заказов клиента",
        )(self.all_client_order)
        self.router.get(
            f"{AppPathConstants.PaginateClientOrderPathName}",
            response_model=PaginationOrderWithRelationsDTO,
            summary="Пагинация заказов клиента",
            description="Пагинация списка заказов клиента",
        )(self.paginate_client_order)
        self.router.get(
            f"{AppPathConstants.GetClientOrderByIdPathName}",
            response_model=OrderWithRelationsDTO,
            summary="Получить заказ клиента по идентфикатору",
            description="Получение заказа клиента по идентфикатору",
        )(self.get_client_order_by_id)
        self.router.get(
            f"{AppPathConstants.GetClientOrderByValuePathName}",
            response_model=OrderWithRelationsDTO,
            summary="Получить заказ клиента по значению",
            description="Получение заказа клиента по значению",
        )(self.get_client_order_by_value)

    async def create_client_order(
        self,
        dto: CreateOrderDTO,
        user: UserWithRelationsDTO = Depends(check_client),
        db: AsyncSession = Depends(get_db),
    ):
        use_case = CreateClientOrderCase(db)
        sap_case = CreateClientSapOrderCase(db)
        update_order_case = AddSapIdToOrderCase(db)
        try:
            order = await use_case.execute(dto=dto, user=user)
            if app_config.sap_create_order_after_order:
                sap_request = await sap_case.execute(order_id=order.id, user=user)
                order = await update_order_case.execute(
                    sap_id=sap_request.id, user=user
                )
            return order
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            error_details = traceback.format_exc()
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании заказа",
                extra={"details": f"{str(exc)}"},
                is_custom=True,
            )

    async def all_client_order(
        self,
        parameters: OrderClientFilter = Depends(),
        user: UserWithRelationsDTO = Depends(check_client),
        db: AsyncSession = Depends(get_db),
    ):
        use_case = AllClientOrderCase(db)
        try:
            order = await use_case.execute(parameters=parameters, user=user)
            return order
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании заказа",
                extra={"details": f"{str(exc)}"},
                is_custom=True,
            )

    async def paginate_client_order(
        self,
        parameters: OrderClientFilter = Depends(),
        user: UserWithRelationsDTO = Depends(check_client),
        db: AsyncSession = Depends(get_db),
    ):
        use_case = PaginateClientOrderCase(db)
        try:
            order = await use_case.execute(filter=parameters, user=user)
            return order
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при создании заказа",
                extra={"details": f"{str(exc)}"},
                is_custom=True,
            )

    async def get_client_order_by_id(
        self,
        id: AppPathConstants.IDPath,
        user: UserWithRelationsDTO = Depends(check_client),
        db: AsyncSession = Depends(get_db),
    ):
        use_case = GetClientOrderByIdCase(db)
        try:
            order = await use_case.execute(id=id, user=user)
            return order
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении заказа",
                extra={"details": f"{str(exc)}"},
                is_custom=True,
            )

    async def get_client_order_by_value(
        self,
        value: AppPathConstants.ValuePath,
        user: UserWithRelationsDTO = Depends(check_client),
        db: AsyncSession = Depends(get_db),
    ):
        use_case = GetClientOrderByValueCase(db)
        try:
            order = await use_case.execute(value=value, user=user)
            return order
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении заказа",
                extra={"details": f"{str(exc)}"},
                is_custom=True,
            )
