from operator import and_

from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.workshop_schedule.workshop_schedule_dto import (
    WorkshopScheduleCDTO, WorkshopScheduleWithRelationsDTO)
from app.adapters.repositories.workshop.workshop_repository import \
    WorkshopRepository
from app.adapters.repositories.workshop_schdedule.workshop_schedule_repository import \
    WorkshopScheduleRepository
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class UpdateWorkshopScheduleCase(BaseUseCase[WorkshopScheduleWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = WorkshopScheduleRepository(db)
        self.workshop_repository = WorkshopRepository(db)

    async def execute(
        self, id: int, dto: WorkshopScheduleCDTO
    ) -> WorkshopScheduleWithRelationsDTO:
        obj = await self.validate(id=id, dto=dto)
        data = await self.repository.update(obj=obj, dto=dto)
        if not data:
            raise AppExceptionResponse.bad_request(message="Расписание не обновлено")
        existed = await self.repository.get(
            id=data.id,
            options=self.repository.default_relationships(),
        )
        return WorkshopScheduleWithRelationsDTO.from_orm(existed)

    async def validate(self, id: int, dto: WorkshopScheduleCDTO):
        existed_schedule = self.repository.get(id)
        if not existed_schedule:
            raise AppExceptionResponse.not_found(message="Расписание цеха не найдено")
        existed = await self.repository.get_first_with_filters(
            filters=[
                and_(
                    self.repository.model.start_at <= dto.start_at,
                    self.repository.model.end_at >= dto.start_at,
                    self.repository.model.is_active.is_(True),
                    self.repository.model.workshop_id == dto.workshop_id,
                    self.repository.model.id != id,
                )
            ]
        )
        if existed:
            raise AppExceptionResponse.bad_request(
                "Активное расписание цеха уже существует"
            )
        existed_workshop = await self.workshop_repository.get(id=dto.workshop_id)
        if not existed_workshop:
            raise AppExceptionResponse.bad_request("Цех с таким id не найден")
        if existed_workshop.sap_id != dto.workshop_sap_id:
            raise AppExceptionResponse.bad_request("Значение SAP Id цеха неверно")
        dto.workshop_sap_id = existed_workshop.sap_id
        return existed_schedule
