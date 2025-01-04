from typing import List, Optional

from sqlalchemy import and_, inspect, or_
from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_pagination_filter import BasePaginationFilter
from app.entities import OrganizationModel
from app.shared.query_constants import AppQueryConstants


class OrganizationFilter(BasePaginationFilter[OrganizationModel]):
    def __init__(
        self,
        per_page: int = AppQueryConstants.StandardPerPageQuery(),
        page: int = AppQueryConstants.StandardPageQuery(),
        search: Optional[str] = AppQueryConstants.StandardOptionalSearchQuery(
            description="Уникальный поиск по наименованию, БИН, БИК, email, телефону"
        ),
        order_by: Optional[str] = AppQueryConstants.StandardSortFieldQuery(),
        order_direction: Optional[str] = AppQueryConstants.StandardSortDirectionQuery(),
        owner_ids: Optional[
            list[int]
        ] = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            description="Поиск по ID владельцам"
        ),
        type_ids: Optional[
            list[int]
        ] = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            description="Поиск по типам пользователя"
        ),
        status: Optional[bool] = AppQueryConstants.StandardOptionalBooleanQuery(
            description="Статус активности"
        ),
    ):
        super().__init__(
            model=OrganizationModel,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
            page=page,
            per_page=per_page,
        )
        self.owner_ids = owner_ids
        self.type_ids = type_ids
        self.status = status

    def get_search_filters(self) -> Optional[List[str]]:
        return [
            "full_name",
            "short_name",
            "bin",
            "bik",
            "kbe",
            "email",
            "phone",
            "address",
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
        if self.owner_ids:
            filters.append(and_(self.model.owner_id.in_(self.owner_ids)))
        if self.type_ids:
            filters.append(and_(self.model.type_id.in_(self.type_ids)))
        if self.status is not None:
            filters.append(and_(self.model.status == self.status))
        return filters
