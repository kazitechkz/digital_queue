from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.workshop_schedule.workshop_schedule_dto import \
    WorkshopScheduleWithRelationsDTO
from app.adapters.repositories.workshop_schdedule.workshop_schedule_repository import \
    WorkshopScheduleRepository
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class GetWorkshopScheduleByIdCase(BaseUseCase[WorkshopScheduleWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = WorkshopScheduleRepository(db)

    async def execute(self, id: int) -> WorkshopScheduleWithRelationsDTO:
        model = await self.repository.get(
            id, options=self.repository.default_relationships()
        )
        if not model:
            raise AppExceptionResponse.not_found("Расписание цеха не найдено")
        return WorkshopScheduleWithRelationsDTO.from_orm(model)

    async def validate(self):
        pass
