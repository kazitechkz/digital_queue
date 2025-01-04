from datetime import datetime
from typing import List, Optional

from sqlalchemy import and_, inspect, or_
from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_pagination_filter import BasePaginationFilter
from app.entities import VerifiedVehicleModel
from app.shared.query_constants import AppQueryConstants


class VerifiedVehicleFilter(BasePaginationFilter[VerifiedVehicleModel]):
    def __init__(
        self,
        per_page: int = AppQueryConstants.StandardPerPageQuery(),
        page: int = AppQueryConstants.StandardPageQuery(),
        search: Optional[str] = AppQueryConstants.StandardOptionalSearchQuery(
            description="Уникальный поиск по идентификатору, Номеру машины, Описанию, Ответу, Верифицировавшему"
        ),
        order_by: Optional[str] = AppQueryConstants.StandardSortFieldQuery(),
        order_direction: Optional[str] = AppQueryConstants.StandardSortDirectionQuery(),
        is_active: bool = AppQueryConstants.StandardOptionalBooleanQuery(
            description="Активно"
        ),
    ):
        super().__init__(
            model=VerifiedVehicleModel,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
            page=page,
            per_page=per_page,
        )
        self.is_active = is_active

    def get_search_filters(self) -> Optional[List[str]]:
        return [
            "car_number",
            "verified_by",
            "verified_by_sid",
            "description",
            "response",
        ]

    def apply(self) -> List[SQLAlchemyQuery]:
        now = datetime.now()
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
        if self.is_active is not None:
            filters.append(
                and_(self.model.is_verified == True, self.model.will_act_at > now)
            )
        return filters
