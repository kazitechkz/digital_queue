from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.vehicle_category.vehicle_category_dto import (
    VehicleCategoryCDTO,
    VehicleCategoryRDTO,
)
from app.adapters.repositories.vehicle_category.vehicle_category_repository import (
    VehicleCategoryRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class CreateVehicleCategoryCase(BaseUseCase[VehicleCategoryRDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = VehicleCategoryRepository(db)

    async def execute(self, dto: VehicleCategoryCDTO) -> VehicleCategoryRDTO:
        obj = await self.validate(dto=dto)
        data = await self.repository.create(obj=obj)
        return VehicleCategoryRDTO.from_orm(data)

    async def validate(self, dto: VehicleCategoryCDTO):
        existed = await self.repository.get_first_with_filters(
            filters=[func.lower(self.repository.model.value) == dto.value.lower()]
        )
        if existed:
            raise AppExceptionResponse.bad_request(
                "Категория ТС с таким значением уже существует"
            )
        return self.repository.model(**dto.dict())
