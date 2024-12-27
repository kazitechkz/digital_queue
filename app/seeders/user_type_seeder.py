from sqlalchemy.ext.asyncio import AsyncSession

from app.entities import OrganizationTypeModel, UserTypeModel
from app.seeders.base_seeder import BaseSeeder
from app.shared.app_constants import AppTableNames
from app.shared.db_constants import AppDbValueConstants


class UserTypeSeeder(BaseSeeder):
    async def seed(self, session: AsyncSession):
        data = self.get_data()
        await self.load_seeders(
            UserTypeModel, session, AppTableNames.UserTypeTableName, data
        )

    def get_dev_data(self):
        return [
            UserTypeModel(
                title="Физическое лицо",
                value=AppDbValueConstants.INDIVIDUAL_VALUE,
                keycloak_id=AppDbValueConstants.INDIVIDUAL_VALUE,
                keycloak_value=AppDbValueConstants.INDIVIDUAL_VALUE,
                is_active=True,
            ),
            UserTypeModel(
                title="Юридическое лицо",
                value=AppDbValueConstants.LEGAL_VALUE,
                keycloak_id=AppDbValueConstants.LEGAL_VALUE,
                keycloak_value=AppDbValueConstants.LEGAL_VALUE,
                is_active=True,
            ),
        ]

    def get_prod_data(self):
        return self.get_dev_data()

    def get_dev_updated_data(self):
        pass

    def get_prod_updated_data(self):
        pass
