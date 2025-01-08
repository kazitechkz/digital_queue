from typing import List, Optional

from sqlalchemy import and_, inspect, or_, select
from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.adapters.filters.base_pagination_filter import BasePaginationFilter
from app.core.app_exception_response import AppExceptionResponse
from app.entities import VehicleModel
from app.shared.query_constants import AppQueryConstants


class VehicleClientFilter(BasePaginationFilter[VehicleModel]):
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
        owner_id: Optional[
            int
        ] = AppQueryConstants.StandardOptionalIntegerQuery(
            description="Поиск по владельцу"
        ),
        organization_ids: Optional[
            list[int]
        ] = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            description="Поиск по организациям"
        ),
        is_trailer: Optional[bool] = AppQueryConstants.StandardOptionalBooleanQuery(
            description="Трейлер?"
        ),
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
        self.owner_id = owner_id
        self.organization_ids = organization_ids
        self.is_trailer = is_trailer

    def get_search_filters(self) -> Optional[List[str]]:
        return [
            "registration_number",
            "car_model",
            "vehicle_info",
        ]

    def apply(self,user:UserWithRelationsDTO,check_verified:bool = False) -> List[SQLAlchemyQuery]:
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
        if self.owner_id:
            if self.owner_id != user.id:
                raise AppExceptionResponse().bad_request("Вы не можете просматривать ТС других пользователей")
            filters.append(and_(self.model.owner_id == self.owner_id))
        if self.organization_ids and user.organizations:
            valid_ids = {org.id for org in user.organizations}
            invalid_ids = [org_id for org_id in self.organization_ids if org_id not in valid_ids]
            if invalid_ids:
                raise AppExceptionResponse().bad_request("Вы не можете просматривать ТС других организаций")
            filters.append(and_(self.model.organization_id.in_(self.organization_ids)))
        if self.is_trailer is not None:
            filters.append(and_(self.model.is_trailer == self.is_trailer))
        return filters
