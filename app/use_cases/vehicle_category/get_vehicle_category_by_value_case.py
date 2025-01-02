from sqlalchemy import and_, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.vehicle_category.vehicle_category_dto import VehicleCategoryRDTO
from app.adapters.repositories.vehicle_category.vehicle_category_repository import (
    VehicleCategoryRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class GetVehicleCategoryByValueCase(BaseUseCase[VehicleCategoryRDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = VehicleCategoryRepository(db)

    async def execute(self, value: str) -> VehicleCategoryRDTO:
        filters = [
            and_(
                func.lower(self.repository.model.value) == value.lower(),
            )
        ]
        model = await self.repository.get_first_with_filters(filters=filters)
        if not model:
            raise AppExceptionResponse.not_found("Категория ТС не найдена")
        return VehicleCategoryRDTO.from_orm(model)

    async def validate(self):
        pass
