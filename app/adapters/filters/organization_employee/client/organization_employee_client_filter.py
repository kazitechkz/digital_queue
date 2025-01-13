from typing import List, Optional

from sqlalchemy import and_, inspect, or_
from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.adapters.filters.base_pagination_filter import BasePaginationFilter
from app.entities import OrganizationEmployeeModel
from app.shared.db_constants import AppDbValueConstants
from app.shared.query_constants import AppQueryConstants


class OrganizationEmployeeClientFilter(BasePaginationFilter[OrganizationEmployeeModel]):
    def __init__(
        self,
        per_page: int = AppQueryConstants.StandardPerPageQuery(),
        page: int = AppQueryConstants.StandardPageQuery(),
        search: Optional[str] = AppQueryConstants.StandardOptionalSearchQuery(
            description="Уникальный поиск по БИН, SID"
        ),
        order_by: Optional[str] = AppQueryConstants.StandardSortFieldQuery(),
        order_direction: Optional[str] = AppQueryConstants.StandardSortDirectionQuery(),
        employee_ids: Optional[
            list[int]
        ] = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            description="Поиск по ID работников"
        ),
        organization_ids: Optional[
            list[int]
        ] = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            description="Поиск по ID организаций"
        ),
        request_ids: Optional[
            list[int]
        ] = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            description="Поиск по ID заявкам"
        ),
    ):
        super().__init__(
            model=OrganizationEmployeeModel,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
            page=page,
            per_page=per_page,
        )
        self.employee_ids = employee_ids
        self.organization_ids = organization_ids
        self.request_ids = request_ids

    def get_search_filters(self) -> Optional[List[str]]:
        return [
            "bin",
            "sid",
        ]

    def apply(self, user: UserWithRelationsDTO) -> List[SQLAlchemyQuery]:
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
        if user.user_type.value == AppDbValueConstants.LEGAL_VALUE:
            organization_ids = [org.id for org in user.organizations]
            filters.append(and_(self.model.organization_id.in_(organization_ids)))
        else:
            filters.append(and_(self.model.employee_id == user.id))
        if self.employee_ids:
            filters.append(and_(self.model.employee_id.in_(self.employee_ids)))
        if self.organization_ids:
            filters.append(and_(self.model.organization_id.in_(self.organization_ids)))
        if self.request_ids:
            filters.append(and_(self.model.request_id.in_(self.request_ids)))
        return filters
