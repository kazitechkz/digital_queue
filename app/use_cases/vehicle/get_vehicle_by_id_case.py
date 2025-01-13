from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.dto.vehicle.vehicle_dto import VehicleWithRelationsDTO
from app.adapters.repositories.vehicle.vehicle_repository import VehicleRepository
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class GetVehicleByIdCase(BaseUseCase[VehicleWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = VehicleRepository(db)

    async def execute(self, id: int) -> VehicleWithRelationsDTO:
        model = await self.repository.get(
            id,
            options=self.repository.default_relationships(),
        )
        if not model:
            raise AppExceptionResponse.not_found("тс не найден")
        return VehicleWithRelationsDTO.from_orm(model)

    async def validate(self):
        pass
