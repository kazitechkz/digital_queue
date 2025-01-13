from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repositories.base_repository import BaseRepository
from app.entities import SapRequestModel


class SapRequestRepository(BaseRepository[SapRequestModel]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(SapRequestModel, db)
