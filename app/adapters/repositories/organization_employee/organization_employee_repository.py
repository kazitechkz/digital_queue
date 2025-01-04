from typing import List, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.repositories.base_repository import BaseRepository
from app.entities import OrganizationEmployeeModel


class OrganizationEmployeeRepository(BaseRepository[OrganizationEmployeeModel]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(OrganizationEmployeeModel, db)

    def default_relationships(self) -> List[Any]:
        return [
            selectinload(self.model.employee),
            selectinload(self.model.organization),
            selectinload(self.model.request),
        ]
