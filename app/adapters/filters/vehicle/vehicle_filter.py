from typing import List, Optional

from sqlalchemy import and_, inspect, or_, select
from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_pagination_filter import BasePaginationFilter
from app.entities import OrganizationModel, UserModel, VehicleModel
from app.shared.query_constants import AppQueryConstants


class VehicleFilter(BasePaginationFilter[VehicleModel]):
    def __init__(
        self,
        per_page: int = AppQueryConstants.StandardPerPageQuery(),
        page: int = AppQueryConstants.StandardPageQuery(),
        search: Optional[str] = AppQueryConstants.StandardOptionalSearchQuery(
            description="Уникальный поиск по Номеру ТС, модели, инфорамации транспорта"
        ),
        order_by: Optional[str] = AppQueryConstants.StandardSortFieldQuery(),
        order_direction: Optional[str] = AppQueryConstants.StandardSortDirectionQuery(),
        category_ids: Optional[
            list[int]
        ] = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            description="Поиск по категориям"
        ),
        colors_ids: Optional[
            list[int]
        ] = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            description="Поиск по цветам"
        ),
        owner_ids: Optional[
            list[int]
        ] = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            description="Поиск по владельцам"
        ),
        organization_ids: Optional[
            list[int]
        ] = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            description="Поиск по организациям"
        ),
        is_trailer: Optional[bool] = AppQueryConstants.StandardOptionalBooleanQuery(
            description="Трейлер?"
        ),
        owner_iin: Optional[str] = AppQueryConstants.StandardOptionalIINQuery(),
        organization_bin: Optional[str] = AppQueryConstants.StandardOptionalBINQuery(),
    ):
        super().__init__(
            model=VehicleModel,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
            page=page,
            per_page=per_page,
        )
        self.category_ids = category_ids
        self.colors_ids = colors_ids
        self.owner_ids = owner_ids
        self.organization_ids = organization_ids
        self.is_trailer = is_trailer
        self.owner_iin = owner_iin
        self.organization_bin = organization_bin

    def get_search_filters(self) -> Optional[List[str]]:
        return [
            "registration_number",
            "car_model",
            "vehicle_info",
        ]

    def apply(self) -> List[SQLAlchemyQuery]:
        filters = []
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
        if self.category_ids:
            filters.append(and_(self.model.category_id.in_(self.category_ids)))
        if self.colors_ids:
            filters.append(and_(self.model.color_id.in_(self.colors_ids)))
        if self.owner_ids:
            filters.append(and_(self.model.owner_id.in_(self.owner_ids)))
        if self.organization_ids:
            filters.append(and_(self.model.organization_id.in_(self.organization_ids)))
        if self.is_trailer is not None:
            filters.append(and_(self.model.is_trailer == self.is_trailer))
        if self.owner_iin:
            filters.append(self.model.owner.has(UserModel.iin == self.owner_iin))
        if self.organization_bin:
            filters.append(
                self.model.organization.has(
                    OrganizationModel.bin == self.organization_bin
                )
            )
        return filters
