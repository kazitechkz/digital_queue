from typing import Any, List

from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.repositories.base_repository import BaseRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import OperationModel


class OperationRepository(BaseRepository[OperationModel]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(OperationModel, db)

    def default_relationships(self) -> List[Any]:
        return [
            selectinload(self.model.prev_operation),
            selectinload(self.model.next_operation),
            selectinload(self.model.role),
        ]

    async def first_operation(self):
        model = await self.get_first_with_filters(
            filters=[
                and_(self.model.is_first == True)
            ]
        )
        if not model:
            raise AppExceptionResponse.internal_error("Первичный процесс не создан")
        if not model.is_active:
            return await self.next_operation(current_operation_id=model.next_id)
        return model
    async def next_operation(self,current_operation_id:int):
        model = await self.get(id=current_operation_id)
        if not model:
            raise AppExceptionResponse.internal_error("Операция не найдена")
        if not model.is_active and not model.is_first and not model.is_last:
            return await self.next_operation(current_operation_id=model.next_id)
        return model


