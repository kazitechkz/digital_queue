from sqlalchemy.ext.asyncio import AsyncSession

from app.entities import VehicleCategoryModel
from app.seeders.base_seeder import BaseSeeder
from app.shared.app_constants import AppTableNames


class VehicleCategorySeeder(BaseSeeder):
    async def seed(self, session: AsyncSession):
        data = self.get_data()
        await self.load_seeders(
            VehicleCategoryModel, session, AppTableNames.VehicleCategoryTableName, data
        )

    def get_dev_data(self):
        return [
            VehicleCategoryModel(title="C", value="c"),
            VehicleCategoryModel(title="CE", value="ce"),
            VehicleCategoryModel(title="C1", value="c1"),
            VehicleCategoryModel(title="C1E", value="c1e"),
        ]

    def get_prod_data(self):
        return self.get_dev_data()

    def get_dev_updated_data(self):
        pass

    def get_prod_updated_data(self):
        pass
