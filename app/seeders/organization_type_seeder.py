from sqlalchemy.ext.asyncio import AsyncSession

from app.entities import OrganizationTypeModel
from app.entities.role import RoleModel
from app.seeders.base_seeder import BaseSeeder
from app.shared.app_constants import AppTableNames
from app.shared.db_constants import AppDbValueConstants


class OrganizationTypeSeeder(BaseSeeder):
    async def seed(self, session: AsyncSession):
        data = self.get_data()
        await self.load_seeders(
            OrganizationTypeModel,
            session,
            AppTableNames.OrganizationTypeTableName,
            data,
        )

    def get_dev_data(self):
        return [
            OrganizationTypeModel(
                title="Товарищество с ограниченной ответственностью",
                value=AppDbValueConstants.LLP_VALUE,
            ),
            OrganizationTypeModel(
                title="Индивидуальный предприниматель",
                value=AppDbValueConstants.IE_VALUE,
            ),
            OrganizationTypeModel(
                title="Акционерное общество",
                value=AppDbValueConstants.JCS_VALUE,
            ),
            OrganizationTypeModel(
                title="Государственная корпорация",
                value=AppDbValueConstants.SC_VALUE,
            ),
            OrganizationTypeModel(
                title="Крестьянское хозяйство",
                value=AppDbValueConstants.FE_VALUE,
            ),
            OrganizationTypeModel(
                title="Производственный кооператив",
                value=AppDbValueConstants.PC_VALUE,
            ),
            OrganizationTypeModel(
                title="Некоммерческое Акционерное Общество",
                value=AppDbValueConstants.NON_JCS_VALUE,
            ),
        ]

    def get_prod_data(self):
        return self.get_dev_data()

    def get_dev_updated_data(self):
        pass

    def get_prod_updated_data(self):
        pass
