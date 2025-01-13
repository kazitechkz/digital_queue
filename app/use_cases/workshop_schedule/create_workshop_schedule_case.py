from sqlalchemy import and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.workshop_schedule.workshop_schedule_dto import (
    WorkshopScheduleCDTO,
    WorkshopScheduleWithRelationsDTO,
)
from app.adapters.repositories.workshop.workshop_repository import WorkshopRepository
from app.adapters.repositories.workshop_schdedule.workshop_schedule_repository import (
    WorkshopScheduleRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class CreateWorkshopScheduleCase(BaseUseCase[WorkshopScheduleWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = WorkshopScheduleRepository(db)
        self.workshop_repository = WorkshopRepository(db)

    async def execute(
        self, dto: WorkshopScheduleCDTO
    ) -> WorkshopScheduleWithRelationsDTO:
        obj = await self.validate(dto=dto)
        data = await self.repository.create(obj=obj)
        if not data:
            raise AppExceptionResponse.bad_request(message="Расписание не создано")
        existed = await self.repository.get(
            id=data.id,
            options=self.repository.default_relationships(),
        )
        return WorkshopScheduleWithRelationsDTO.from_orm(existed)

    async def validate(self, dto: WorkshopScheduleCDTO):
        existed = await self.repository.get_first_with_filters(
            filters=[
                and_(
                    self.repository.model.start_at <= dto.start_at,
                    self.repository.model.end_at >= dto.start_at,
                    self.repository.model.is_active.is_(True),
                    self.repository.model.workshop_id == dto.workshop_id,
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
        dto.workshop_sap_id = existed_workshop.sap_id
        return self.repository.model(**dto.dict())
