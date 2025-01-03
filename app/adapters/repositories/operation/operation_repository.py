from typing import Any, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.repositories.base_repository import BaseRepository
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
