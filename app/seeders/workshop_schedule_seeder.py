from datetime import date, time

from sqlalchemy.ext.asyncio import AsyncSession

from app.entities import WorkshopScheduleModel
from app.seeders.base_seeder import BaseSeeder
from app.shared.app_constants import AppTableNames


class WorkshopScheduleSeeder(BaseSeeder):
    async def seed(self, session: AsyncSession):
        data = self.get_data()
        await self.load_seeders(
            WorkshopScheduleModel,
            session,
            AppTableNames.WorkshopScheduleTableName,
            data,
        )

    def get_dev_data(self):
        # Пример данных
        data = [
            {
                "workshop_id": 1,
                "workshop_sap_id": "5404",
                "date_start": "2024-01-01",
                "date_end": "2024-12-31",
                "start_at": "09:00:00",
                "end_at": "20:00:00",
                "car_service_min": 20,
                "break_between_service_min": 5,
                "machine_at_one_time": 4,
                "is_active": True,
            },
            {
                "workshop_id": 2,
                "workshop_sap_id": "5407",
                "date_start": "2024-01-01",
                "date_end": "2024-12-31",
                "start_at": "09:00:00",
                "end_at": "18:00:00",
                "car_service_min": 15,
                "break_between_service_min": 0,
                "machine_at_one_time": 2,
                "is_active": True,
            },
        ]

        # Модели для вставки
        workshop_schedules = [
            WorkshopScheduleModel(
                workshop_id=item["workshop_id"],
                workshop_sap_id=item["workshop_sap_id"],
                date_start=date.fromisoformat(item["date_start"]),
                date_end=date.fromisoformat(item["date_end"]),
                start_at=time.fromisoformat(item["start_at"]),
                end_at=time.fromisoformat(item["end_at"]),
                car_service_min=item["car_service_min"],
                break_between_service_min=item["break_between_service_min"],
                machine_at_one_time=item["machine_at_one_time"],
                can_earlier_come_min=0,  # Default value
                can_late_come_min=0,  # Default value
                is_active=item["is_active"],
            )
            for item in data
        ]
        return workshop_schedules

    def get_prod_data(self):
        return self.get_dev_data()

    def get_dev_updated_data(self):
        pass

    def get_prod_updated_data(self):
        pass
