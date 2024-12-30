from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repositories.base_repository import BaseRepository
from app.entities import RoleModel


class RoleRepository(BaseRepository[RoleModel]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(RoleModel, db)
