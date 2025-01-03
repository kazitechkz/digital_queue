from typing import Any, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.repositories.base_repository import BaseRepository
from app.entities import MaterialModel


class MaterialRepository(BaseRepository[MaterialModel]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(MaterialModel, db)

    def default_relationships(self) -> List[Any]:
        return [
            selectinload(self.model.file),
            selectinload(self.model.workshop),
        ]
