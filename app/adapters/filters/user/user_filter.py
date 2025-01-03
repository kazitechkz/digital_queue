from typing import List, Optional

from fastapi import Depends
from sqlalchemy import and_, inspect, or_
from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_pagination_filter import BasePaginationFilter
from app.entities import UserModel
from app.shared.query_constants import AppQueryConstants


class UserFilter(BasePaginationFilter[UserModel]):
    def __init__(
        self,
        per_page: int = AppQueryConstants.StandardPerPageQuery(),
        page: int = AppQueryConstants.StandardPageQuery(),
        search: Optional[str] = AppQueryConstants.StandardOptionalSearchQuery(
            description="Уникальный поиск по идентификатору, ИИН, ФИО, email, телефону"
        ),
        order_by: Optional[str] = AppQueryConstants.StandardSortFieldQuery(),
        order_direction: Optional[str] = AppQueryConstants.StandardSortDirectionQuery(),
        role_ids: Optional[
            list[int]
        ] = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            description="Поиск по ролям"
        ),
        type_ids: Optional[
            list[int]
        ] = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            description="Поиск по типам пользователя"
        ),
    ):
        super().__init__(
            model=UserModel,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
            page=page,
            per_page=per_page,
        )
        self.role_ids = role_ids
        self.type_ids = type_ids

    def get_search_filters(self) -> Optional[List[str]]:
        return [
            "sid",
            "iin",
            "name",
            "given_name",
            "family_name",
            "preferred_username",
            "email",
            "phone",
            "tabn",
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
        if self.role_ids:
            filters.append(and_(self.model.role_id.in_(self.role_ids)))
        if self.type_ids:
            filters.append(and_(self.model.type_id.in_(self.type_ids)))
        return filters
