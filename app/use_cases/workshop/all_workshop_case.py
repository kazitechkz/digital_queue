from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.dto.workshop.workshop_dto import WorkshopWithRelationsDTO
from app.adapters.repositories.workshop.workshop_repository import \
    WorkshopRepository
from app.use_cases.base_case import BaseUseCase


class AllWorkshopCase(BaseUseCase[list[WorkshopWithRelationsDTO]]):
    def __init__(self, db: AsyncSession):
        self.repository = WorkshopRepository(db)

    async def execute(self) -> list[WorkshopWithRelationsDTO]:
        models = await self.repository.get_all(
            options=self.repository.default_relationships(),
            order_by="id",
        )
        return [WorkshopWithRelationsDTO.from_orm(model) for model in models]

    async def validate(self):
        pass
