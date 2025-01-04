from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.verified_vehicle.verified_vehicle_dto import (
    VerifiedVehicleCDTO,
    VerifiedVehicleWithRelationsDTO,
)
from app.adapters.repositories.user.user_repository import UserRepository
from app.adapters.repositories.vehicle.vehicle_repository import VehicleRepository
from app.adapters.repositories.verified_vehicle.verified_verticle_repository import (
    VerifiedVehicleRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class CreateVerifiedVehicleCase(BaseUseCase[VerifiedVehicleWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = VerifiedVehicleRepository(db)
        self.vehicle_repository = VehicleRepository(db)

    async def execute(
        self, dto: VerifiedVehicleCDTO
    ) -> VerifiedVehicleWithRelationsDTO:
        obj = await self.validate(dto=dto)
        data = await self.repository.create(obj=obj)
        if not data:
            raise AppExceptionResponse.internal_error("Проверенное ТС не создано")
        existed = await self.repository.get(
            id=data.id,
            options=self.repository.default_relationships(),
        )
        return VerifiedVehicleWithRelationsDTO.from_orm(existed)

    async def validate(self, dto: VerifiedVehicleCDTO):
        existed = await self.vehicle_repository.get(id=dto.vehicle_id)
        if not existed:
            raise AppExceptionResponse.bad_request("ТС не найдено")
        dto.car_number = existed.registration_number
        return self.repository.model(**dto.dict())
