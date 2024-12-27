from sqlalchemy.ext.asyncio import AsyncSession

from app.entities import WorkshopModel
from app.seeders.base_seeder import BaseSeeder
from app.shared.app_constants import AppTableNames


class WorkshopSeeder(BaseSeeder):
    async def seed(self, session: AsyncSession):
        data = self.get_data()
        await self.load_seeders(
            WorkshopModel, session, AppTableNames.WorkshopTableName, data
        )

    def get_dev_data(self):
        return [
            WorkshopModel(
                title="Цех 5404",
                description="Цех 5404",
                sap_id="5404",
                status=True,
                factory_id=1,
                factory_sap_id="1011",
            ),
            WorkshopModel(
                title="Цех 5407",
                description="Цех 5407",
                sap_id="5407",
                status=True,
                factory_id=1,
                factory_sap_id="1023",
            ),
        ]

    def get_prod_data(self):
        return self.get_dev_data()

    def get_dev_updated_data(self):
        pass

    def get_prod_updated_data(self):
        pass
