from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.vehicle_color.vehicle_color_dto import VehicleColorRDTO
from app.adapters.repositories.vehicle_color.vehicle_color_repository import (
    VehicleColorRepository,
)
from app.use_cases.base_case import BaseUseCase


class AllVehicleColorCase(BaseUseCase[list[VehicleColorRDTO]]):
    def __init__(self, db: AsyncSession):
        self.repository = VehicleColorRepository(db)

    async def execute(self) -> list[VehicleColorRDTO]:
        models = await self.repository.get_all()
        return [VehicleColorRDTO.from_orm(model) for model in models]

    async def validate(self):
        pass
