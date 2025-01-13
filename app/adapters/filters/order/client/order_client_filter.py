from typing import List, Optional

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
        status_values: Optional[List[str]] = None,
        status_ids: Optional[List[int]] = None,
        factory_ids: Optional[List[int]] = None,
        workshop_ids: Optional[List[int]] = None,
        material_ids: Optional[List[int]] = None,
        executed_cruise_gt: Optional[int] = None,
        price_gt: Optional[int] = None,
        sap_id: Optional[int] = None,
        kaspi_id: Optional[int] = None,
        is_active: Optional[bool] = None,
        is_finished: Optional[bool] = None,
        is_failed: Optional[bool] = None,
        is_paid: Optional[bool] = None,
        is_cancel: Optional[bool] = None,
    ):
        super().__init__(
            model=OrderModel,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
            page=page,
            per_page=per_page,
        )
        self.status_values = status_values
        self.status_ids = status_ids
        self.factory_ids = factory_ids
        self.workshop_ids = workshop_ids
        self.material_ids = material_ids
        self.executed_cruise_gt = executed_cruise_gt
        self.price_gt = price_gt
        self.sap_id = sap_id
        self.kaspi_id = kaspi_id
        self.is_active = is_active
        self.is_finished = is_finished
        self.is_failed = is_failed
        self.is_paid = is_paid
        self.is_cancel = is_cancel

    def get_search_filters(self) -> List[str]:
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

    def apply(self, user: UserWithRelationsDTO) -> List[SQLAlchemyQuery]:
        filters = [
            or_(
                self.model.owner_id == user.id,
                self.model.iin == user.iin,
                self.model.owner_sid == user.sid,
            )
        ]

        # Поиск по строке
        if self.search:
            model_columns = {column.key for column in inspect(self.model).columns}
            valid_fields = [
                field for field in self.get_search_filters() if field in model_columns
            ]
            if valid_fields:
                filters.append(
                    or_(
                        *[
                            getattr(self.model, field).like(f"%{self.search}%")
                            for field in valid_fields
                        ]
                    )
                )

        # Автоматическая генерация фильтров
        conditions = [
            (self.status_values, self.model.status.in_),
            (self.status_ids, self.model.status_id.in_),
            (self.factory_ids, self.model.factory_id.in_),
            (self.workshop_ids, self.model.workshop_id.in_),
            (self.material_ids, self.model.material_id.in_),
            (self.executed_cruise_gt, lambda x: self.model.executed_cruise > x),
            (self.price_gt, lambda x: self.model.price_with_taxes > x),
            (self.sap_id, lambda x: self.model.factory_sap_id == x),
            (self.kaspi_id, lambda x: self.model.kaspi_id == x),
            (self.is_active, lambda x: self.model.is_active == x),
            (self.is_finished, lambda x: self.model.is_finished == x),
            (self.is_failed, lambda x: self.model.is_failed == x),
            (self.is_paid, lambda x: self.model.is_paid == x),
            (self.is_cancel, lambda x: self.model.is_cancel == x),
        ]

        for value, condition in conditions:
            if value is not None:
                filters.append(condition(value))

        return filters
