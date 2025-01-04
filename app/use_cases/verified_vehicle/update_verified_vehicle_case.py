from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.verified_vehicle.verified_vehicle_dto import (
    VerifiedVehicleCDTO, VerifiedVehicleWithRelationsDTO)
from app.adapters.repositories.user.user_repository import UserRepository
from app.adapters.repositories.vehicle.vehicle_repository import \
    VehicleRepository
from app.adapters.repositories.verified_vehicle.verified_verticle_repository import \
    VerifiedVehicleRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import VerifiedVehicleModel
from app.use_cases.base_case import BaseUseCase


class UpdateVerifiedVehicleCase(BaseUseCase[VerifiedVehicleWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = VerifiedVehicleRepository(db)
        self.vehicle_repository = VehicleRepository(db)

    async def execute(
        self, id: int, dto: VerifiedVehicleCDTO
    ) -> VerifiedVehicleWithRelationsDTO:
        model = await self.validate(id=id, dto=dto)
        dto = await self.transform(model=model, dto=dto)
        data = await self.repository.update(obj=model, dto=dto)
        if not data:
            raise AppExceptionResponse.internal_error(
                "Проверенный Транспорт не обновлен"
            )
        existed = await self.repository.get(
            id=data.id,
            options=self.repository.default_relationships(),
        )
        return VerifiedVehicleWithRelationsDTO.from_orm(existed)

    async def validate(self, id: int, dto: VerifiedVehicleCDTO) -> VerifiedVehicleModel:
        model = await self.repository.get(id=id)
        if not model:
            raise AppExceptionResponse.not_found(
                message="Проверенный Транспорт не найден"
            )
        existed = await self.vehicle_repository.get(id=dto.user_id)
        if not existed:
            raise AppExceptionResponse.bad_request("Транспорт не найден")
        return model

    async def transform(
        self, model: VerifiedVehicleModel, dto: VerifiedVehicleCDTO
    ) -> VerifiedVehicleWithRelationsDTO:
        dto.car_number = model.car_number
        return dto
