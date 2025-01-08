from typing import Optional, List

from sqlalchemy import or_, inspect, and_
from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.adapters.filters.base_pagination_filter import BasePaginationFilter
from app.entities import EmployeeRequestModel
from app.shared.db_constants import AppDbValueConstants
from app.shared.query_constants import AppQueryConstants


class EmployeeRequestClientFilter(BasePaginationFilter[EmployeeRequestModel]):
    def __init__(
        self,
        per_page: int = AppQueryConstants.StandardPerPageQuery(),
        page: int = AppQueryConstants.StandardPageQuery(),
        search: Optional[str] = AppQueryConstants.StandardOptionalSearchQuery(
            description="Уникальный поиск по идентификатору, ИИН, БИН, компании, работнику, владельцу"
        ),
        order_by: Optional[str] = AppQueryConstants.StandardSortFieldQuery(),
        order_direction: Optional[str] = AppQueryConstants.StandardSortDirectionQuery(),
        status: bool = AppQueryConstants.StandardOptionalIntegerQuery(
            description="Статус ответа 1 - Положительный, 0 - ожидание, -1 - Отказ"
        ),
    ):
        super().__init__(
            model=EmployeeRequestModel,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
            page=page,
            per_page=per_page,
        )
        self.status = status

    def get_search_filters(self) -> Optional[List[str]]:
        return [
            "employee_name",
            "employee_email",
            "employee_sid",
            "organization_full_name",
            "organization_bin",
            "owner_name",
            "owner_sid",
        ]

    def apply(self,user:UserWithRelationsDTO) -> List[SQLAlchemyQuery]:
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
        if self.status:
            filters.append(and_(self.model.status == self.status))
        if user.user_type.value == AppDbValueConstants.LEGAL_VALUE:
            filters.append(and_(self.model.owner_id == user.id))
        else:
            filters.append(and_(self.model.employee_id == user.id))
        return filters