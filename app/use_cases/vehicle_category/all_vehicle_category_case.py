from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.vehicle_category.vehicle_category_dto import \
    VehicleCategoryRDTO
from app.adapters.repositories.vehicle_category.vehicle_category_repository import \
    VehicleCategoryRepository
from app.use_cases.base_case import BaseUseCase


class AllVehicleCategoryCase(BaseUseCase[list[VehicleCategoryRDTO]]):
    def __init__(self, db: AsyncSession):
        self.repository = VehicleCategoryRepository(db)

    async def execute(self) -> list[VehicleCategoryRDTO]:
        models = await self.repository.get_all()
        return [VehicleCategoryRDTO.from_orm(model) for model in models]

    async def validate(self):
        pass
