from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationVehicleWithRelationsDTO
from app.adapters.dto.vehicle.vehicle_dto import VehicleWithRelationsDTO
from app.adapters.filters.vehicle.vehicle_filter import VehicleFilter
from app.adapters.repositories.vehicle.vehicle_repository import VehicleRepository
from app.use_cases.base_case import BaseUseCase


class PaginateVehicleCase(BaseUseCase[PaginationVehicleWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = VehicleRepository(db)

    async def execute(self, filter: VehicleFilter) -> PaginationVehicleWithRelationsDTO:
        models = await self.repository.paginate(
            dto=VehicleWithRelationsDTO,
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