from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.vehicle_color.vehicle_color_dto import (
    VehicleColorCDTO,
    VehicleColorRDTO,
)
from app.adapters.repositories.vehicle_color.vehicle_color_repository import (
    VehicleColorRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class CreateVehicleColorCase(BaseUseCase[VehicleColorRDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = VehicleColorRepository(db)

    async def execute(self, dto: VehicleColorCDTO) -> VehicleColorRDTO:
        obj = await self.validate(dto=dto)
        data = await self.repository.create(obj=obj)
        return VehicleColorRDTO.from_orm(data)

    async def validate(self, dto: VehicleColorCDTO):
        existed = await self.repository.get_first_with_filters(
            filters=[func.lower(self.repository.model.value) == dto.value.lower()]
        )
        if existed:
            raise AppExceptionResponse.bad_request(
                "Цвет ТС с таким значением уже существует"
            )
        return self.repository.model(**dto.dict())
