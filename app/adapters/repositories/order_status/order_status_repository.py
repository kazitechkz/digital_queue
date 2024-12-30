from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repositories.base_repository import BaseRepository
from app.entities import OrderStatusModel


class OrderStatusRepository(BaseRepository[OrderStatusModel]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(OrderStatusModel, db)
