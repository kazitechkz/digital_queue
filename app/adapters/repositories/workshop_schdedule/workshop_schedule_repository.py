from typing import Any, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.repositories.base_repository import BaseRepository
from app.entities import WorkshopScheduleModel


class WorkshopScheduleRepository(BaseRepository[WorkshopScheduleModel]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(WorkshopScheduleModel, db)

    def default_relationships(self) -> List[Any]:
        return [
            selectinload(self.model.workshop),
        ]
