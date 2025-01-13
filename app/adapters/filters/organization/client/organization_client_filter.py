from typing import List, Optional

from sqlalchemy import and_, inspect, or_
from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_pagination_filter import BasePaginationFilter
from app.entities import OrganizationModel
from app.shared.query_constants import AppQueryConstants


class OrganizationClientFilter(BasePaginationFilter[OrganizationModel]):
    def __init__(
        self,
        per_page: int = AppQueryConstants.StandardPerPageQuery(),
        page: int = AppQueryConstants.StandardPageQuery(),
        search: Optional[str] = AppQueryConstants.StandardOptionalSearchQuery(
            description="Уникальный поиск по наименованию, БИН, БИК, email, телефону"
        ),
        order_by: Optional[str] = AppQueryConstants.StandardSortFieldQuery(),
        order_direction: Optional[str] = AppQueryConstants.StandardSortDirectionQuery(),
        type_ids: Optional[
            list[int]
        ] = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            description="Поиск по типам пользователя"
        ),
        status: Optional[bool] = AppQueryConstants.StandardOptionalBooleanQuery(
            description="Статус активности"
        ),
        is_verified: Optional[bool] = AppQueryConstants.StandardOptionalBooleanQuery(
            description="Подтвержден ли модератором"
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
        self.type_ids = type_ids
        self.status = status
        self.is_verified = is_verified

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

    def apply(self, client_id: int) -> List[SQLAlchemyQuery]:
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
        filters.append(and_(self.model.owner_id == client_id))
        if self.type_ids:
            filters.append(and_(self.model.type_id.in_(self.type_ids)))
        if self.status is not None:
            filters.append(and_(self.model.status == self.status))
        if self.is_verified is not None:
            filters.append(and_(self.model.is_verified == self.is_verified))
        return filters
