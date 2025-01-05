from typing import Any, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.repositories.base_repository import BaseRepository
from app.entities import UserModel


class UserRepository(BaseRepository[UserModel]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(UserModel, db)

    def default_relationships(self) -> List[Any]:
        return [
            selectinload(self.model.role),
            selectinload(self.model.file),
            selectinload(self.model.user_type),
            selectinload(self.model.organizations)
        ]
