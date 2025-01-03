from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.vehicle_category.vehicle_category_dto import (
    VehicleCategoryCDTO, VehicleCategoryRDTO)
from app.adapters.repositories.vehicle_category.vehicle_category_repository import \
    VehicleCategoryRepository
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class UpdateVehicleCategoryCase(BaseUseCase[VehicleCategoryRDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = VehicleCategoryRepository(db)

    async def execute(self, id: int, dto: VehicleCategoryCDTO) -> VehicleCategoryRDTO:
        obj = await self.validate(id=id, dto=dto)
        data = await self.repository.update(obj=obj, dto=dto)
        return VehicleCategoryRDTO.from_orm(data)

    async def validate(self, id: int, dto: VehicleCategoryCDTO):
        existed = await self.repository.get(id=id)
        if existed is None:
            raise AppExceptionResponse.not_found(message="Категория ТС не найдена")
        if await self.repository.get_first_with_filters(
            [
                func.lower(self.repository.model.value) == dto.value.lower(),
                self.repository.model.id != id,
            ]
        ):
            raise AppExceptionResponse.bad_request(
                "Категория ТС с таким значением уже существует"
            )
        return existed
