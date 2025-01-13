from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.workshop_schedule.workshop_schedule_dto import (
    WorkshopScheduleWithRelationsDTO,
)
from app.adapters.repositories.workshop_schdedule.workshop_schedule_repository import (
    WorkshopScheduleRepository,
)
from app.use_cases.base_case import BaseUseCase


class AllWorkshopScheduleCase(BaseUseCase[list[WorkshopScheduleWithRelationsDTO]]):
    def __init__(self, db: AsyncSession):
        self.repository = WorkshopScheduleRepository(db)

    async def execute(self) -> list[WorkshopScheduleWithRelationsDTO]:
        models = await self.repository.get_all(
            options=self.repository.default_relationships()
        )
        return [WorkshopScheduleWithRelationsDTO.from_orm(model) for model in models]

    async def validate(self):
        pass
