from sqlalchemy import and_, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.vehicle.vehicle_dto import VehicleWithRelationsDTO
from app.adapters.repositories.vehicle.vehicle_repository import \
    VehicleRepository
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class GetVehicleByValueCase(BaseUseCase[VehicleWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = VehicleRepository(db)

    async def execute(self, value: str) -> VehicleWithRelationsDTO:
        filters = [
            or_(
                func.lower(self.repository.model.registration_number) == value.lower(),
            )
        ]
        model = await self.repository.get_first_with_filters(
            filters=filters,
            options=self.repository.default_relationships(),
        )
        if not model:
            raise AppExceptionResponse.not_found("ТС не найдено")
        return VehicleWithRelationsDTO.from_orm(model)

    async def validate(self):
        pass
