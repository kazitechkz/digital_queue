from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.dto.workshop.workshop_dto import WorkshopWithRelationsDTO
from app.adapters.repositories.workshop.workshop_repository import \
    WorkshopRepository
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class GetWorkshopByIdCase(BaseUseCase[WorkshopWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = WorkshopRepository(db)

    async def execute(self, id: int) -> WorkshopWithRelationsDTO:
        model = await self.repository.get(
            id,
            options=self.repository.default_relationships(),
        )
        if not model:
            raise AppExceptionResponse.not_found("Цех не найден")
        return WorkshopWithRelationsDTO.from_orm(model)

    async def validate(self):
        pass
