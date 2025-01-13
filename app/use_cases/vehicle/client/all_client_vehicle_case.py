from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.user.user_dto import UserWithRelationsDTO
from app.adapters.dto.vehicle.vehicle_dto import VehicleWithRelationsDTO
from app.adapters.filters.vehicle.client.vehicle_client_filter import (
    VehicleClientFilter,
)
from app.adapters.repositories.vehicle.vehicle_repository import VehicleRepository
from app.use_cases.base_case import BaseUseCase


class AllClientVehicleCase(BaseUseCase[List[VehicleWithRelationsDTO]]):
    def __init__(self, db: AsyncSession):
        self.repository = VehicleRepository(db)

    async def execute(
        self, filter: VehicleClientFilter, user: UserWithRelationsDTO
    ) -> List[VehicleWithRelationsDTO]:
        models = await self.repository.get_with_filters(
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            options=self.repository.default_relationships(),
            filters=filter.apply(user=user),
        )
        return [VehicleWithRelationsDTO.from_orm(model) for model in models]

    async def validate(self):
        pass
