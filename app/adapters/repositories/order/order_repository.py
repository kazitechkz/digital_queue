from typing import Any, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.repositories.base_repository import BaseRepository
from app.entities import OrderModel


class OrderRepository(BaseRepository[OrderModel]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(OrderModel, db)

    def default_relationships(self) -> List[Any]:
        return [
            selectinload(self.model.factory),
            selectinload(self.model.workshop),
            selectinload(self.model.material),
            selectinload(self.model.sap),
            selectinload(self.model.kaspi),
            selectinload(self.model.owner),
            selectinload(self.model.organization),
            selectinload(self.model.canceled_by),
            selectinload(self.model.checked_payment_by),
            selectinload(self.model.payment_return),
            selectinload(self.model.order_status),
        ]
