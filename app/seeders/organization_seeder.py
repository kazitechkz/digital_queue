from sqlalchemy.ext.asyncio import AsyncSession

from app.entities import OrganizationModel
from app.seeders.base_seeder import BaseSeeder
from app.shared.app_constants import AppTableNames


class OrganizationSeeder(BaseSeeder):
    async def seed(self, session: AsyncSession):
        data = self.get_data()
        await self.load_seeders(
            OrganizationModel, session, AppTableNames.OrganizationTableName, data
        )

    def get_dev_data(self):
        return [
            OrganizationModel(
                id=1,
                file_id=None,
                full_name="ТОО 'KAZ ITECH'",
                short_name="KAZ ITECH",
                bin="230540028470",
                bik="BRKEKZKZ",
                kbe="KZ45914122203KZ00557",
                email="kazitech2023@gmail.com",
                phone="+77064205961",
                address="Астана Мангилик Ел",
                status=True,
                owner_id=2,
                type_id=1,
            ),
            OrganizationModel(
                id=2,
                file_id=None,
                full_name="ТОО 'I-UNION'",
                short_name="I-UNION",
                bin="220640051457",
                bik="BRKEKZKG",
                kbe="KZ459141222034560557",
                email="iunion@gmail.com",
                phone="+77054171796",
                address="Астана Мангилик Ел",
                status=True,
                owner_id=3,
                type_id=1,
            ),
        ]

    def get_prod_data(self):
        return self.get_data()

    def get_dev_updated_data(self):
        pass

    def get_prod_updated_data(self):
        pass
