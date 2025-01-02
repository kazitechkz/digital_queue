from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.dto.material.material_dto import MaterialWithRelationsDTO
from app.adapters.repositories.material.material_repository import MaterialRepository
from app.use_cases.base_case import BaseUseCase


class AllMaterialCase(BaseUseCase[list[MaterialWithRelationsDTO]]):
    def __init__(self, db: AsyncSession):
        self.repository = MaterialRepository(db)

    async def execute(self) -> list[MaterialWithRelationsDTO]:
        models = await self.repository.get_all(
            options=[
                selectinload(self.repository.model.file),
                selectinload(self.repository.model.workshop),
            ],
            order_by="id",
        )
        return [MaterialWithRelationsDTO.from_orm(model) for model in models]

    async def validate(self):
        pass
