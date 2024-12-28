from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.role import RoleModel
from app.seeders.base_seeder import BaseSeeder
from app.shared.app_constants import AppTableNames
from app.shared.db_constants import AppDbValueConstants


class RoleSeeder(BaseSeeder):
    async def seed(self, session: AsyncSession):
        roles = self.get_data()
        await self.load_seeders(RoleModel, session, AppTableNames.RoleTableName, roles)

    def get_dev_data(self):
        return [
            RoleModel(
                id=1,
                title="Администратор",
                value=AppDbValueConstants.ADMINISTRATOR_VALUE,
                keycloak_id=AppDbValueConstants.ADMINISTRATOR_KEYCLOAK_VALUE,
                keycloak_value=AppDbValueConstants.ADMINISTRATOR_KEYCLOAK_VALUE,
                is_active=True,
            ),
            RoleModel(
                id=2,
                title="Служба Безопасности",
                value=AppDbValueConstants.SECURITY_VALUE,
                keycloak_id=AppDbValueConstants.SECURITY_KEYCLOAK_VALUE,
                keycloak_value=AppDbValueConstants.SECURITY_KEYCLOAK_VALUE,
                is_active=True,
            ),
            RoleModel(
                id=3,
                title="Контроллер погрузки",
                value=AppDbValueConstants.SECURITY_LOADER_VALUE,
                keycloak_id=AppDbValueConstants.SECURITY_LOADER_KEYCLOAK_VALUE,
                keycloak_value=AppDbValueConstants.SECURITY_LOADER_KEYCLOAK_VALUE,
                is_active=True,
            ),
            RoleModel(
                id=4,
                title="Погрузчик",
                value=AppDbValueConstants.LOADER_VALUE,
                keycloak_id=AppDbValueConstants.LOADER_KEYCLOAK_VALUE,
                keycloak_value=AppDbValueConstants.LOADER_KEYCLOAK_VALUE,
                is_active=True,
            ),
            RoleModel(
                id=5,
                title="Весовщик",
                value=AppDbValueConstants.WEIGHER_VALUE,
                keycloak_id=AppDbValueConstants.WEIGHER_KEYCLOAK_VALUE,
                keycloak_value=AppDbValueConstants.WEIGHER_KEYCLOAK_VALUE,
                is_active=True,
            ),
            RoleModel(
                id=6,
                title="Менеджер",
                value=AppDbValueConstants.MANAGER_VALUE,
                keycloak_id=AppDbValueConstants.MANAGER_KEYCLOAK_VALUE,
                keycloak_value=AppDbValueConstants.MANAGER_KEYCLOAK_VALUE,
                is_active=True,
            ),
            RoleModel(
                id=7,
                title="Клиент",
                value=AppDbValueConstants.CLIENT_VALUE,
                keycloak_id=AppDbValueConstants.CLIENT_KEYCLOAK_VALUE,
                keycloak_value=AppDbValueConstants.CLIENT_KEYCLOAK_VALUE,
                is_active=True,
            ),
        ]

    def get_prod_data(self):
        return self.get_dev_data()

    def get_dev_updated_data(self):
        pass

    def get_prod_updated_data(self):
        pass
