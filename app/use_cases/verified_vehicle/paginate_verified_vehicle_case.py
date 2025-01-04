from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationVerifiedVehicleWithRelationsDTO
from app.adapters.dto.verified_vehicle.verified_vehicle_dto import (
    VerifiedVehicleWithRelationsDTO,
)
from app.adapters.filters.verified_vehicle.verified_vehicle_filter import (
    VerifiedVehicleFilter,
)
from app.adapters.repositories.verified_vehicle.verified_verticle_repository import (
    VerifiedVehicleRepository,
)
from app.use_cases.base_case import BaseUseCase


class PaginateVerifiedVehicleCase(
    BaseUseCase[PaginationVerifiedVehicleWithRelationsDTO]
):
    def __init__(self, db: AsyncSession):
        self.repository = VerifiedVehicleRepository(db)

    async def execute(
        self, filter: VerifiedVehicleFilter
    ) -> PaginationVerifiedVehicleWithRelationsDTO:
        models = await self.repository.paginate(
            dto=VerifiedVehicleWithRelationsDTO,
            page=filter.page,
            per_page=filter.per_page,
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            options=self.repository.default_relationships(),
            filters=filter.apply(),
        )
        return models

    async def validate(self):
        pass
