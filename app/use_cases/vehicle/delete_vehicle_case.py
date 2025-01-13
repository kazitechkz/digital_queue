from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repositories.vehicle.vehicle_repository import VehicleRepository
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.services.file_service import FileService
from app.use_cases.base_case import BaseUseCase


class DeleteVehicleCase(BaseUseCase[bool]):
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = VehicleRepository(db)
        self.service = FileService(db)

    async def execute(self, id: int) -> bool:
        await self.validate(id=id)
        data = await self.repository.delete(id=id)
        return data

    async def validate(self, id: int):
        existed = await self.repository.get(id=id)
        if existed is None:
            raise AppExceptionResponse.not_found(message="ТС не найдено")
        if existed.file_id:
            await self.service.delete_file(db=self.db, file_id=existed.file_id)
