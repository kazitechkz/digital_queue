from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repositories.vehicle_color.vehicle_color_repository import \
    VehicleColorRepository
from app.core.app_exception_response import AppExceptionResponse
from app.shared.db_constants import AppDbValueConstants
from app.use_cases.base_case import BaseUseCase


class DeleteVehicleColorCase(BaseUseCase[bool]):
    def __init__(self, db: AsyncSession):
        self.repository = VehicleColorRepository(db)

    async def execute(self, id: int) -> bool:
        await self.validate(id=id)
        data = await self.repository.delete(id=id)
        return data

    async def validate(self, id: int):
        existed = await self.repository.get(id=id)
        if existed is None:
            raise AppExceptionResponse.not_found(message="Цвет ТС не найден")