from typing import Any, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.repositories.base_repository import BaseRepository
from app.entities import OrderStatusModel


class OrderStatusRepository(BaseRepository[OrderStatusModel]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(OrderStatusModel, db)

    def default_relationships(self) -> List[Any]:
        return [
            selectinload(self.model.prev_order_status),
            selectinload(self.model.next_order_status),
        ]
