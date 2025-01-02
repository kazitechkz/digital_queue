from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.dto.material.material_dto import MaterialWithRelationsDTO
from app.adapters.repositories.material.material_repository import MaterialRepository
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class GetMaterialByIdCase(BaseUseCase[MaterialWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = MaterialRepository(db)

    async def execute(self, id: int) -> MaterialWithRelationsDTO:
        model = await self.repository.get(
            id,
            options=[
                selectinload(self.repository.model.file),
                selectinload(self.repository.model.workshop),
            ],
        )
        if not model:
            raise AppExceptionResponse.not_found("Материал не найден")
        return MaterialWithRelationsDTO.from_orm(model)

    async def validate(self):
        pass
