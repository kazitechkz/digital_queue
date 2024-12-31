from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.dto.operation.operation_dto import OperationWithRelationsDTO
from app.adapters.repositories.operation.operation_repository import \
    OperationRepository
from app.use_cases.base_case import BaseUseCase


class AllOperationCase(BaseUseCase[list[OperationWithRelationsDTO]]):
    def __init__(self, db: AsyncSession):
        self.repository = OperationRepository(db)

    async def execute(self) -> list[OperationWithRelationsDTO]:
        models = await self.repository.get_all(
            options=[
                selectinload(self.repository.model.prev_operation),
                selectinload(self.repository.model.next_operation),
                selectinload(self.repository.model.role),
            ],
            order_by="id",
        )
        print(models)
        return [OperationWithRelationsDTO.from_orm(model) for model in models]

    async def validate(self):
        pass
