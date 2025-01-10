from typing import Optional, List
from sqlalchemy import and_, inspect, or_
from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.adapters.filters.base_pagination_filter import BasePaginationFilter
from app.entities import OrderModel
from app.shared.query_constants import AppQueryConstants


class OrderClientFilter(BasePaginationFilter[OrderModel]):
    def __init__(
            self,
            per_page: int = AppQueryConstants.StandardPerPageQuery(),
            page: int = AppQueryConstants.StandardPageQuery(),
            search: Optional[str] = AppQueryConstants.StandardOptionalSearchQuery(
                description="Уникальный поиск по наименованию, БИН, БИК, email, телефону"
            ),
            order_by: Optional[str] = AppQueryConstants.StandardSortFieldQuery(),
            order_direction: Optional[str] = AppQueryConstants.StandardSortDirectionQuery(),
            status_values:Optional[List[str]] = AppQueryConstants.StandardOptionalStringArrayQuery(
                description="Поиск по значением статуса заказа"
            ),
            status_ids:Optional[List[int]] = AppQueryConstants.StandardOptionalIntegerArrayQuery(
                description="Поиск по ID статуса заказа"
            ),
            factory_ids: Optional[List[int]] = AppQueryConstants.StandardOptionalIntegerArrayQuery(
                description="Поиск по ID заводов"
            ),
            workshop_ids: Optional[List[int]] = AppQueryConstants.StandardOptionalIntegerArrayQuery(
                description="Поиск по ID цехов"
            ),
            material_ids: Optional[List[int]] = AppQueryConstants.StandardOptionalIntegerArrayQuery(
                description="Поиск по ID материалов"
            ),
            executed_cruise_gt:Optional[int] = AppQueryConstants.StandardOptionalIntegerQuery(
                description="Поиск по количеству выполненного круиза больше"
            ),
            price_gt: Optional[int] = AppQueryConstants.StandardOptionalIntegerQuery(
                description="Поиск по сумме KZT больше"
            ),
            sap_id: Optional[int] = AppQueryConstants.StandardOptionalIntegerQuery(
                description="Поиск по номеру сапа"
            ),
            kaspi_id: Optional[int] = AppQueryConstants.StandardOptionalIntegerQuery(
                description="Поиск по номеру каспи"
            ),
            is_active: Optional[bool] = AppQueryConstants.StandardOptionalBooleanQuery(
                description="Активный заказ?"
            ),
            is_finished: Optional[bool] = AppQueryConstants.StandardOptionalBooleanQuery(
                description="Завершен ли?"
            ),
            is_failed: Optional[bool] = AppQueryConstants.StandardOptionalBooleanQuery(
                description="Провален ли?"
            ),
            is_paid: Optional[bool] = AppQueryConstants.StandardOptionalBooleanQuery(
                description="Оплачен ли?"
            ),
            is_cancel: Optional[bool] = AppQueryConstants.StandardOptionalBooleanQuery(
                description="Отменен ли?"
            )
    ):
        super().__init__(
            model=OrderModel,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
            page=page,
            per_page=per_page,
        )
        self.status_values = status_values,
        self.status_ids = status_ids,
        self.factory_ids = factory_ids,
        self.workshop_ids = workshop_ids,
        self.material_ids = material_ids,
        self.executed_cruise_gt = executed_cruise_gt,
        self.price_gt = price_gt,
        self.sap_id = sap_id,
        self.kaspi_id = kaspi_id,
        self.is_active = is_active,
        self.is_finished = is_finished,
        self.is_failed = is_failed,
        self.is_paid = is_paid,
        self.is_cancel = is_cancel


    def get_search_filters(self) -> Optional[List[str]]:
            return [
                "status",
                "factory_sap_id",
                "workshop_sap_id",
                "material_sap_id",
                "zakaz",
                "txn_id",
                "iin",
                "owner_sid",
                "owner_username",
                "owner_email",
                "owner_mobile",
                "name",
                "adr_index",
                "adr_city",
                "adr_str",
                "adr_dom",
                "bin",
                "dogovor",
                "canceled_by_sid",
                "checked_payment_by",
            ]

    def apply(self,user:UserWithRelationsDTO) -> List[SQLAlchemyQuery]:
        filters = []
        filters.append(and_(
            or_(
                self.model.owner_id == user.id,
                self.model.iin == user.iin,
                self.model.owner_sid == user.sid,
            )
        ))
        if self.search:
            # Проверяем существование полей в модели
            model_columns = {column.key for column in inspect(self.model).columns}
            search_fields = self.get_search_filters()
            valid_fields = [field for field in search_fields if field in model_columns]
            if valid_fields:
                filters.append(
                    or_(
                        *[
                            getattr(self.model, field).like(f"%{self.search}%")
                            for field in valid_fields
                        ]
                    )
                )
        if self.status_values:
            filters.append(and_(self.model.status.in_(self.status_values)))
        if self.status_ids:
            filters.append(and_(self.model.status_id.in_(self.status_ids)))
        if self.factory_ids:
            filters.append(and_(self.model.factory_id.in_(self.factory_ids)))
        if self.workshop_ids:
            filters.append(and_(self.model.workshop_id.in_(self.workshop_ids)))
        if self.material_ids:
            filters.append(and_(self.model.material_id.in_(self.material_ids)))
        if self.executed_cruise_gt:
            filters.append(and_(self.model.executed_cruise > self.executed_cruise_gt))
        if self.price_gt:
            filters.append(and_(self.model.price_with_taxes > self.price_gt))
        if self.sap_id:
            filters.append(and_(self.model.factory_sap_id == self.sap_id))
        if self.kaspi_id:
            filters.append(and_(self.model.kaspi_id == self.kaspi_id))
        if self.is_active is not None:
            filters.append(and_(self.model.is_active == self.is_active))
        if self.is_finished is not None:
            filters.append(and_(self.model.is_finished == self.is_finished))
        if self.is_failed is not None:
            filters.append(and_(self.model.is_failed == self.is_failed))
        if self.is_paid is not None:
            filters.append(and_(self.model.is_paid == self.is_paid))
        if self.is_cancel is not None:
            filters.append(and_(self.model.is_cancel == self.is_cancel))

        return filters