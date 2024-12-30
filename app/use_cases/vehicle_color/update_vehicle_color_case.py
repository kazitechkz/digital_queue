from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.vehicle_color.vehicle_color_dto import (VehicleColorCDTO,
                                                              VehicleColorRDTO)
from app.adapters.repositories.vehicle_color.vehicle_color_repository import \
    VehicleColorRepository
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class UpdateVehicleColorCase(BaseUseCase[VehicleColorRDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = VehicleColorRepository(db)

    async def execute(self, id: int, dto: VehicleColorCDTO) -> VehicleColorRDTO:
        obj = await self.validate(id=id, dto=dto)
        data = await self.repository.update(obj=obj, dto=dto)
        return VehicleColorRDTO.from_orm(data)

    async def validate(self, id: int, dto: VehicleColorCDTO):
        existed = await self.repository.get(id=id)
        if existed is None:
            raise AppExceptionResponse.not_found(message="Цвет ТС не найден")
        if await self.repository.get_first_with_filters(
            [
                func.lower(self.repository.model.value) == dto.value.lower(),
                self.repository.model.id != id,
            ]
        ):
            raise AppExceptionResponse.bad_request(
                "Цвет ТС с таким значением уже существует"
            )
        return existed
