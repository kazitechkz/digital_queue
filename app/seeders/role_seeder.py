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
                title="Администратор",
                value=AppDbValueConstants.ADMINISTRATOR_VALUE,
                keycloak_id=AppDbValueConstants.ADMINISTRATOR_KEYCLOAK_VALUE,
                keycloak_value=AppDbValueConstants.ADMINISTRATOR_KEYCLOAK_VALUE,
                is_active=True,
            ),
            RoleModel(
                title="Служба Безопасности",
                value=AppDbValueConstants.SECURITY_VALUE,
                keycloak_id=AppDbValueConstants.SECURITY_KEYCLOAK_VALUE,
                keycloak_value=AppDbValueConstants.SECURITY_KEYCLOAK_VALUE,
                is_active=True,
            ),
            RoleModel(
                title="Контроллер погрузки",
                value=AppDbValueConstants.SECURITY_LOADER_VALUE,
                keycloak_id=AppDbValueConstants.SECURITY_LOADER_KEYCLOAK_VALUE,
                keycloak_value=AppDbValueConstants.SECURITY_LOADER_KEYCLOAK_VALUE,
                is_active=True,
            ),
            RoleModel(
                title="Погрузчик",
                value=AppDbValueConstants.LOADER_VALUE,
                keycloak_id=AppDbValueConstants.LOADER_KEYCLOAK_VALUE,
                keycloak_value=AppDbValueConstants.LOADER_KEYCLOAK_VALUE,
                is_active=True,
            ),
            RoleModel(
                title="Весовщик",
                value=AppDbValueConstants.WEIGHER_VALUE,
                keycloak_id=AppDbValueConstants.WEIGHER_KEYCLOAK_VALUE,
                keycloak_value=AppDbValueConstants.WEIGHER_KEYCLOAK_VALUE,
                is_active=True,
            ),
            RoleModel(
                title="Менеджер",
                value=AppDbValueConstants.MANAGER_VALUE,
                keycloak_id=AppDbValueConstants.MANAGER_KEYCLOAK_VALUE,
                keycloak_value=AppDbValueConstants.MANAGER_KEYCLOAK_VALUE,
                is_active=True,
            ),
            RoleModel(
                title="Клиент",
                value=AppDbValueConstants.CLIENT_VALUE,
                keycloak_id=AppDbValueConstants.CLIENT_KEYCLOAK_VALUE,
                keycloak_value=AppDbValueConstants.CLIENT_KEYCLOAK_VALUE,
                is_active=True,
            )
        ]

    def get_prod_data(self):
        return [
            RoleModel(
                title="Администратор",
                value=AppDbValueConstants.ADMINISTRATOR_VALUE,
                keycloak_id=AppDbValueConstants.ADMINISTRATOR_KEYCLOAK_VALUE,
                keycloak_value=AppDbValueConstants.ADMINISTRATOR_KEYCLOAK_VALUE,
                is_active=True,
            ),
            RoleModel(
                title="Служба Безопасности",
                value=AppDbValueConstants.SECURITY_VALUE,
                keycloak_id=AppDbValueConstants.SECURITY_KEYCLOAK_VALUE,
                keycloak_value=AppDbValueConstants.SECURITY_KEYCLOAK_VALUE,
                is_active=True,
            ),
            RoleModel(
                title="Контроллер погрузки",
                value=AppDbValueConstants.SECURITY_LOADER_VALUE,
                keycloak_id=AppDbValueConstants.SECURITY_LOADER_KEYCLOAK_VALUE,
                keycloak_value=AppDbValueConstants.SECURITY_LOADER_KEYCLOAK_VALUE,
                is_active=True,
            ),
            RoleModel(
                title="Погрузчик",
                value=AppDbValueConstants.LOADER_VALUE,
                keycloak_id=AppDbValueConstants.LOADER_KEYCLOAK_VALUE,
                keycloak_value=AppDbValueConstants.LOADER_KEYCLOAK_VALUE,
                is_active=True,
            ),
            RoleModel(
                title="Весовщик",
                value=AppDbValueConstants.WEIGHER_VALUE,
                keycloak_id=AppDbValueConstants.WEIGHER_KEYCLOAK_VALUE,
                keycloak_value=AppDbValueConstants.WEIGHER_KEYCLOAK_VALUE,
                is_active=True,
            ),
            RoleModel(
                title="Менеджер",
                value=AppDbValueConstants.MANAGER_VALUE,
                keycloak_id=AppDbValueConstants.MANAGER_KEYCLOAK_VALUE,
                keycloak_value=AppDbValueConstants.MANAGER_KEYCLOAK_VALUE,
                is_active=True,
            ),
            RoleModel(
                title="Клиент",
                value=AppDbValueConstants.CLIENT_VALUE,
                keycloak_id=AppDbValueConstants.CLIENT_KEYCLOAK_VALUE,
                keycloak_value=AppDbValueConstants.CLIENT_KEYCLOAK_VALUE,
                is_active=True,
            )
        ]
