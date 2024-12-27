from sqlalchemy.ext.asyncio import AsyncSession

from app.entities import MaterialModel
from app.seeders.base_seeder import BaseSeeder
from app.shared.app_constants import AppTableNames


class MaterialSeeder(BaseSeeder):
    async def seed(self, session: AsyncSession):
        data = self.get_data()
        await self.load_seeders(
            MaterialModel, session, AppTableNames.MaterialTableName, data
        )

    def get_dev_data(self):
        return [
            MaterialModel(
                title="ПЕСОК ИЗ ШЛАКОВ ВУ ФЕРРОХРОМА 0-5",
                sap_id="30012553",
                price_without_taxes=800.0,
                price_with_taxes=896.0,
                workshop_id=1,
                workshop_sap_id="5404",
                status=True,
                description="Песок из шлаков, фракция 0-5 мм",
            ),
            MaterialModel(
                title="ЩЕБЕНЬ ИЗ ШЛАКОВ ВУ ФЕРРОХРОМА 5-20",
                sap_id="80000620",
                price_without_taxes=725.0,
                price_with_taxes=812.0,
                workshop_id=1,
                workshop_sap_id="5404",
                status=True,
                description="Щебень из шлаков, фракция 5-20 мм",
            ),
            MaterialModel(
                title="ЩЕБЕНЬ ИЗ ШЛАКОВ ВУ ФЕРРОХРОМА 20-40",
                sap_id="30133840",
                price_without_taxes=275.0,
                price_with_taxes=308.0,
                workshop_id=1,
                workshop_sap_id="5404",
                status=True,
                description="Щебень из шлаков, фракция 20-40 мм",
            ),
            MaterialModel(
                title="ПЕСОК ИЗ ШЛАКА ВУ ФХ ОПШ ПЦ№4",
                sap_id="80000860",
                price_without_taxes=800.0,
                price_with_taxes=896.0,
                workshop_id=2,
                workshop_sap_id="5407",
                status=True,
                description="Песок из шлаков ПЦ№4",
            ),
            MaterialModel(
                title="ЩЕБЕНЬ 5-20 ИЗ ШЛАКА ВУ ФХ ОПШ ПЦ№4",
                sap_id="80000861",
                price_without_taxes=178.57,
                price_with_taxes=200.0,
                workshop_id=2,
                workshop_sap_id="5407",
                status=True,
                description="Щебень 5-20 из шлака ПЦ№4",
            ),
            MaterialModel(
                title="ЩЕБЕНЬ 20-40 ИЗ ШЛАКА ВУ ФХ ОПШ ПЦ№4",
                sap_id="80000862",
                price_without_taxes=178.57,
                price_with_taxes=200.0,
                workshop_id=2,
                workshop_sap_id="5407",
                status=True,
                description="Щебень 20-40 из шлака ПЦ№4",
            ),
            MaterialModel(
                title="ЩЕБЕНЬ ШЛАКОВЫЙ ДЛЯ ДОР. СТРОИТ 40-70",
                sap_id="80000575",
                price_without_taxes=178.57,
                price_with_taxes=200.0,
                workshop_id=2,
                workshop_sap_id="5407",
                status=True,
                description="Щебень шлаковый для дорожного строительства, фракция 40-70 мм",
            ),
            MaterialModel(
                title="ШЛАК КАМЕНЬ БУТОВЫЙ ВУ ФХ",
                sap_id="30144621",
                price_without_taxes=250.0,
                price_with_taxes=280.0,
                workshop_id=2,
                workshop_sap_id="5407",
                status=True,
                description="Шлак-камень бутовый",
            ),
        ]

    def get_prod_data(self):
        return self.get_dev_data()

    def get_dev_updated_data(self):
        pass

    def get_prod_updated_data(self):
        pass
