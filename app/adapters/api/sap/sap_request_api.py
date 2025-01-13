import traceback

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.order.order_dto import OrderWithRelationsDTO
from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.core.api_middleware_core import check_client
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.database import get_db
from app.shared.path_constants import AppPathConstants
from app.use_cases.order.client.add_sap_id_to_order_case import AddSapIdToOrderCase
from app.use_cases.sap.client.create_client_sap_order_case import (
    CreateClientSapOrderCase,
)


class SapRequestApi:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.post(
            f"{AppPathConstants.RecreateSAPOrderRequestPathName}",
            response_model=OrderWithRelationsDTO,
            summary="Пересоздать заказ SAP",
            description="Создание заказа SAP",
        )(self.recreate_sap_order)

    async def recreate_sap_order(
        self,
        order_id: AppPathConstants.IDPath,
        user: UserWithRelationsDTO = Depends(check_client),
        db: AsyncSession = Depends(get_db),
    ):
        sap_case = CreateClientSapOrderCase(db)
        update_order_case = AddSapIdToOrderCase(db)
        try:
            sap_request = await sap_case.execute(order_id=order_id, user=user)
            order = await update_order_case.execute(sap_id=sap_request.id, user=user)
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
