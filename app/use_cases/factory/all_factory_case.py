from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.dto.factory.factory_dto import FactoryWithRelationsDTO
from app.adapters.repositories.factory.factory_repository import \
    FactoryRepository
from app.use_cases.base_case import BaseUseCase


class AllFactoryCase(BaseUseCase[list[FactoryWithRelationsDTO]]):
    def __init__(self, db: AsyncSession):
        self.repository = FactoryRepository(db)

    async def execute(self) -> list[FactoryWithRelationsDTO]:
        models = await self.repository.get_all(
            options=self.repository.default_relationships(),
            order_by="id",
        )
        return [FactoryWithRelationsDTO.from_orm(model) for model in models]

    async def validate(self):
        pass
