from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.dto.operation.operation_dto import OperationWithRelationsDTO
from app.adapters.repositories.operation.operation_repository import \
    OperationRepository
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class GetOperationByIdCase(BaseUseCase[OperationWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = OperationRepository(db)

    async def execute(self, id: int) -> OperationWithRelationsDTO:
        model = await self.repository.get(
            id,
            options=self.repository.default_relationships(),
        )
        if not model:
            raise AppExceptionResponse.not_found("Бизнес процесс не найден")
        return OperationWithRelationsDTO.from_orm(model)

    async def validate(self):
        pass
