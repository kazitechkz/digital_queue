from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.vehicle_color.vehicle_color_dto import VehicleColorRDTO
from app.adapters.repositories.vehicle_color.vehicle_color_repository import (
    VehicleColorRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class GetVehicleColorByIdCase(BaseUseCase[VehicleColorRDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = VehicleColorRepository(db)

    async def execute(self, id: int) -> VehicleColorRDTO:
        model = await self.repository.get(id)
        if not model:
            raise AppExceptionResponse.not_found("Цвет ТС не найден")
        return VehicleColorRDTO.from_orm(model)

    async def validate(self):
        pass
