from sqlalchemy import and_, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.dto.operation.operation_dto import OperationWithRelationsDTO
from app.adapters.repositories.operation.operation_repository import \
    OperationRepository
from app.core.app_exception_response import AppExceptionResponse
from app.use_cases.base_case import BaseUseCase


class GetOperationByValueCase(BaseUseCase[OperationWithRelationsDTO]):
    def __init__(self, db: AsyncSession):
        self.repository = OperationRepository(db)

    async def execute(self, value: str) -> OperationWithRelationsDTO:
        filters = [
            and_(
                func.lower(self.repository.model.value) == value.lower(),
            )
        ]
        model = await self.repository.get_first_with_filters(
            filters=filters,
            options=[
                selectinload(self.repository.model.prev_operation),
                selectinload(self.repository.model.next_operation),
                selectinload(self.repository.model.role),
            ],
        )
        if not model:
            raise AppExceptionResponse.not_found("Бизнес процесс не найден")
        return OperationWithRelationsDTO.from_orm(model)

    async def validate(self):
        pass
