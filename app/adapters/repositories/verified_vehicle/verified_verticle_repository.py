from typing import Any, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.repositories.base_repository import BaseRepository
from app.entities import VerifiedVehicleModel


class VerifiedVehicleRepository(BaseRepository[VerifiedVehicleModel]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(VerifiedVehicleModel, db)

    def default_relationships(self) -> List[Any]:
        return [
            selectinload(self.model.vehicle),
        ]
