from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.verified_vehicle.verified_vehicle_dto import (
    VerifiedVehicleWithRelationsDTO,
)
from app.adapters.repositories.verified_vehicle.verified_verticle_repository import (
    VerifiedVehicleRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class GetVerifiedVehicleByIdCase(BaseUseCase[VerifiedVehicleWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = VerifiedVehicleRepository(db)

    async def execute(self, id: int) -> VerifiedVehicleWithRelationsDTO:
        model = await self.repository.get(
            id, options=self.repository.default_relationships()
        )
        if not model:
            raise AppExceptionResponse.not_found("Верифицированное ТС не найдено")
        return VerifiedVehicleWithRelationsDTO.from_orm(model)

    async def validate(self):
        pass
