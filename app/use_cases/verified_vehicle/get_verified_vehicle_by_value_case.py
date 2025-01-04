from sqlalchemy import and_, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.verified_vehicle.verified_vehicle_dto import (
    VerifiedVehicleWithRelationsDTO,
)
from app.adapters.repositories.verified_vehicle.verified_verticle_repository import (
    VerifiedVehicleRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class GetVerifiedVehicleByValueCase(BaseUseCase[VerifiedVehicleWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = VerifiedVehicleRepository(db)

    async def execute(self, value: str) -> VerifiedVehicleWithRelationsDTO:
        filters = [
            or_(
                func.lower(self.repository.model.car_number) == value.lower(),
            )
        ]
        model = await self.repository.get_first_with_filters(
            filters=filters, options=self.repository.default_relationships()
        )
        if not model:
            raise AppExceptionResponse.not_found("Верифицированный транспорт не найден")
        return VerifiedVehicleWithRelationsDTO.from_orm(model)

    async def validate(self):
        pass
