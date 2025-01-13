from typing import Any, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.repositories.base_repository import BaseRepository
from app.entities import ScheduleHistoryModel


class ScheduleHistoryRepository(BaseRepository[ScheduleHistoryModel]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(ScheduleHistoryModel, db)

    def default_relationships(self) -> List[Any]:
        return [
            self.model.schedule,
            self.model.responsible,
            self.model.operation,
            self.model.act_weights,
        ]
