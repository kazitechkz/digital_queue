from sqlalchemy import and_, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.workshop_schedule.workshop_schedule_dto import (
    WorkshopScheduleWithRelationsDTO,
)
from app.adapters.repositories.workshop_schdedule.workshop_schedule_repository import (
    WorkshopScheduleRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class GetWorkshopScheduleByValueCase(BaseUseCase[WorkshopScheduleWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = WorkshopScheduleRepository(db)

    async def execute(self, value: str) -> WorkshopScheduleWithRelationsDTO:
        filters = [
            and_(
                func.lower(self.repository.model.workshop_sap_id) == value.lower(),
            )
        ]
        model = await self.repository.get_first_with_filters(
            filters=filters, options=self.repository.default_relationships()
        )
        if not model:
            raise AppExceptionResponse.not_found("Категория ТС не найдена")
        return WorkshopScheduleWithRelationsDTO.from_orm(model)

    async def validate(self):
        pass
