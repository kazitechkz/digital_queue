from sqlalchemy.ext.asyncio import AsyncSession

from app.entities import VehicleColorModel
from app.seeders.base_seeder import BaseSeeder
from app.shared.app_constants import AppTableNames


class VehicleColorSeeder(BaseSeeder):
    async def seed(self, session: AsyncSession):
        data = self.get_data()
        await self.load_seeders(
            VehicleColorModel, session, AppTableNames.VehicleColorTableName, data
        )

    def get_dev_data(self):
        return [
            VehicleColorModel(title="Красный", value="red"),
            VehicleColorModel(title="Оранжевый", value="orange"),
            VehicleColorModel(title="Жёлтый", value="yellow"),
            VehicleColorModel(title="Зелёный", value="green"),
            VehicleColorModel(title="Голубой", value="light_blue"),
            VehicleColorModel(title="Синий", value="blue"),
            VehicleColorModel(title="Фиолетовый", value="purple"),
            VehicleColorModel(title="Белый", value="white"),
            VehicleColorModel(title="Чёрный", value="black"),
            VehicleColorModel(title="Серый", value="gray"),
            VehicleColorModel(title="Серебристый", value="silver"),
            VehicleColorModel(title="Золотистый", value="gold"),
            VehicleColorModel(title="Комбинированный", value="combined"),
        ]

    def get_prod_data(self):
        return self.get_dev_data()

    def get_dev_updated_data(self):
        pass

    def get_prod_updated_data(self):
        pass
