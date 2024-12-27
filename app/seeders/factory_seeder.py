from sqlalchemy.ext.asyncio import AsyncSession

from app.entities import FactoryModel
from app.seeders.base_seeder import BaseSeeder
from app.shared.app_constants import AppTableNames


class FactorySeeder(BaseSeeder):
    async def seed(self, session: AsyncSession):
        data = self.get_data()
        await self.load_seeders(
            FactoryModel, session, AppTableNames.FactoryTableName, data
        )

    def get_dev_data(self):
        return [
            FactoryModel(
                title="Завод 1011",
                description="Завод 1011",
                sap_id="1011",
                status=True,
            ),
            FactoryModel(
                title="Завод 1023",
                description="Завод 1023",
                sap_id="1023",
                status=True,
            ),
        ]

    def get_prod_data(self):
        return self.get_dev_data()

    def get_dev_updated_data(self):
        pass

    def get_prod_updated_data(self):
        pass
