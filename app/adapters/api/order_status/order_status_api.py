from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.adapters.dto.order_status.order_status_dto import OrderStatusWithRelationsDTO
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.database import get_db
from app.shared.path_constants import AppPathConstants
from app.use_cases.order_status.all_order_status_case import AllOrderStatusCase
from app.use_cases.order_status.get_order_status_by_id_case import GetOrderStatusByIdCase
from app.use_cases.order_status.get_order_status_by_value_case import GetOrderStatusByValueCase


class OrderStatusApi:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            "/",
            response_model=list[OrderStatusWithRelationsDTO],
            summary="Список статусов заказа",
            description="Получение списка статусов заказа",
        )(self.get_all)
        # self.router.post(
        #     "/create",
        #     response_model=OrderStatusRDTO,
        #     summary="Создать тип организации",
        #     description="Создание типа организации",
        # )(self.create)
        # self.router.put(
        #     "/update/{id}",
        #     response_model=OrderStatusRDTO,
        #     summary="Обновить тип организации по уникальному ID",
        #     description="Обновление типа организации по уникальному идентификатору",
        # )(self.update)
        # self.router.delete(
        #     "/delete/{id}",
        #     response_model=bool,
        #     summary="Удалите тип организации по уникальному ID",
        #     description="Удаление типа организации по уникальному идентификатору",
        # )(self.delete)
        self.router.get(
            "/get/{id}",
            response_model=OrderStatusWithRelationsDTO,
            summary="Получить тип организации по уникальному ID",
            description="Получение типа организации по уникальному идентификатору",
        )(self.get)
        self.router.get(
            "/get-by-value/{value}",
            response_model=OrderStatusWithRelationsDTO,
            summary="Получить тип организации по уникальному значению",
            description="Получение типа организации по уникальному значению",
        )(self.get_by_value)

    async def get_all(self, db: AsyncSession = Depends(get_db)):
        use_case = AllOrderStatusCase(db)
        try:
            return await use_case.execute()
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении всех типов",
                extra={"details": str(exc)},
                is_custom=True,
            )

    async def get(
        self, id: AppPathConstants.IDPath, db: AsyncSession = Depends(get_db)
    ):
        use_case = GetOrderStatusByIdCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении типа организации по значению",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            )
    # 
    # async def create(
    #     self, dto: OrderStatusCDTO, db: AsyncSession = Depends(get_db)
    # ):
    #     use_case = CreateOrderStatusCase(db)
    #     try:
    #         return await use_case.execute(dto=dto)
    #     except HTTPException as exc:
    #         raise exc
    #     except Exception as exc:
    #         raise AppExceptionResponse.internal_error(
    #             message="Ошибка при создании типа организации",
    #             extra={"details": str(exc)},
    #             is_custom=True,
    #         )
    # 
    # async def update(
    #     self,
    #     id: AppPathConstants.IDPath,
    #     dto: OrderStatusCDTO,
    #     db: AsyncSession = Depends(get_db),
    # ):
    #     use_case = UpdateOrderStatusCase(db)
    #     try:
    #         return await use_case.execute(id=id, dto=dto)
    #     except HTTPException as exc:
    #         raise exc
    #     except Exception as exc:
    #         raise AppExceptionResponse.internal_error(
    #             message="Ошибка при создании роли",
    #             extra={"id": id, "details": str(exc)},
    #             is_custom=True,
    #         )
    # 
    # async def delete(
    #     self, id: AppPathConstants.IDPath, db: AsyncSession = Depends(get_db)
    # ):
    #     use_case = DeleteOrderStatusCase(db)
    #     try:
    #         return await use_case.execute(id=id)
    #     except HTTPException as exc:
    #         raise exc
    #     except Exception as exc:
    #         raise AppExceptionResponse.internal_error(
    #             message="Ошибка при создании роли",
    #             extra={"id": id, "details": str(exc)},
    #             is_custom=True,
    #         )
    # 
    async def get_by_value(
        self, value: AppPathConstants.ValuePath, db: AsyncSession = Depends(get_db)
    ):
        use_case = GetOrderStatusByValueCase(db)
        try:
            return await use_case.execute(value=value)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при получении типа организации по значению",
                extra={"value": value, "details": str(exc)},
                is_custom=True,
            )
