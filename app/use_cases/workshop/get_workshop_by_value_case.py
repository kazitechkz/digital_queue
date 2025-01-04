from sqlalchemy import and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.dto.workshop.workshop_dto import WorkshopWithRelationsDTO
from app.adapters.repositories.workshop.workshop_repository import \
    WorkshopRepository
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class GetWorkshopByValueCase(BaseUseCase[WorkshopWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = WorkshopRepository(db)

    async def execute(self, value: str) -> WorkshopWithRelationsDTO:
        filters = [
            and_(
                func.lower(self.repository.model.sap_id) == value.lower(),
            )
        ]
        model = await self.repository.get_first_with_filters(
            filters=filters,
            options=self.repository.default_relationships(),
        )
        if not model:
            raise AppExceptionResponse.not_found("Цех не найден")
        return WorkshopWithRelationsDTO.from_orm(model)

    async def validate(self):
        pass
