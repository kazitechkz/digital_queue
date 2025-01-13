from typing import Any, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.repositories.base_repository import BaseRepository
from app.entities import ScheduleModel


class ScheduleRepository(BaseRepository[ScheduleModel]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(ScheduleModel, db)

    def default_relationships(self) -> List[Any]:
        return [
            selectinload(self.model.order),
            selectinload(self.model.owner),
            selectinload(self.model.driver),
            selectinload(self.model.organization),
            selectinload(self.model.vehicle),
            selectinload(self.model.trailer),
            selectinload(self.model.workshop_schedule),
            selectinload(self.model.current_operation),
            selectinload(self.model.responsible),
            selectinload(self.model.canceled_by_user),
            selectinload(self.model.histories),
        ]
