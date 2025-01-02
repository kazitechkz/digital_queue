from sqlalchemy import and_, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.vehicle_color.vehicle_color_dto import VehicleColorRDTO
from app.adapters.repositories.vehicle_color.vehicle_color_repository import (
    VehicleColorRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class GetVehicleColorByValueCase(BaseUseCase[VehicleColorRDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = VehicleColorRepository(db)

    async def execute(self, value: str) -> VehicleColorRDTO:
        filters = [
            and_(
                func.lower(self.repository.model.value) == value.lower(),
            )
        ]
        model = await self.repository.get_first_with_filters(filters=filters)
        if not model:
            raise AppExceptionResponse.not_found("Цвет ТС не найден")
        return VehicleColorRDTO.from_orm(model)

    async def validate(self):
        pass
