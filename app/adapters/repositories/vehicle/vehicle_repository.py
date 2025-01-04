from typing import Any, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.repositories.base_repository import BaseRepository
from app.entities import VehicleModel


class VehicleRepository(BaseRepository[VehicleModel]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(VehicleModel, db)

    def default_relationships(self) -> List[Any]:
        return [
            selectinload(self.model.file),
            selectinload(self.model.owner),
            selectinload(self.model.organization),
            selectinload(self.model.category),
            selectinload(self.model.color),
        ]

    @staticmethod
    def get_vehicle_info(
        car_number: str,
        car_model: str,
        car_category,
        car_color,
    ):
        return (
            f"{car_color.title} {car_model} {car_number.upper()} ({car_category.title})"
        )
