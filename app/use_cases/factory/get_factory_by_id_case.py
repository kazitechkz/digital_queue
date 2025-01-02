from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.dto.factory.factory_dto import FactoryWithRelationsDTO
from app.adapters.repositories.factory.factory_repository import FactoryRepository
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class GetFactoryByIdCase(BaseUseCase[FactoryWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = FactoryRepository(db)

    async def execute(self, id: int) -> FactoryWithRelationsDTO:
        model = await self.repository.get(
            id,
            options=[
                selectinload(self.repository.model.file),
            ],
        )
        if not model:
            raise AppExceptionResponse.not_found("Завод не найден")
        return FactoryWithRelationsDTO.from_orm(model)

    async def validate(self):
        pass
