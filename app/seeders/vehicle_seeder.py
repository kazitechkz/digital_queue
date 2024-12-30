from sqlalchemy.ext.asyncio import AsyncSession

from app.entities import VehicleModel
from app.seeders.base_seeder import BaseSeeder
from app.shared.app_constants import AppTableNames


class VehicleSeeder(BaseSeeder):
    async def seed(self, session: AsyncSession):
        data = self.get_data()
        await self.load_seeders(
            VehicleModel, session, AppTableNames.VehicleTableName, data
        )

    def get_dev_data(self):
        return [
            VehicleModel(
                id=1,
                category_id=1,
                color_id=2,
                owner_id=1,
                organization_id=None,
                file_id=None,
                registration_number="123ABC12",
                car_model="MAN",
                is_trailer=False,
                vehicle_info=None,
            ),
            VehicleModel(
                id=2,
                category_id=2,
                color_id=5,
                owner_id=None,
                organization_id=1,
                file_id=None,
                registration_number="546ABD11",
                car_model="METTLER TOLEDO",
                is_trailer=False,
                vehicle_info=None,
            ),
            VehicleModel(
                id=3,
                category_id=3,
                color_id=8,
                owner_id=None,
                organization_id=2,
                file_id=None,
                registration_number="543DVE12",
                car_model="MERCEDES ACTROS",
                is_trailer=False,
                vehicle_info=None,
            ),
            VehicleModel(
                id=4,
                category_id=1,
                color_id=2,
                owner_id=4,
                organization_id=None,
                file_id=None,
                registration_number="859DDD12",
                car_model="KAMAZ",
                is_trailer=False,
                vehicle_info=None,
            ),
        ]

    def get_prod_data(self):
        return self.get_data()

    def get_dev_updated_data(self):
        pass

    def get_prod_updated_data(self):
        pass
