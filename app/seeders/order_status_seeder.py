from sqlalchemy.ext.asyncio import AsyncSession

from app.entities import OrderStatusModel
from app.seeders.base_seeder import BaseSeeder
from app.shared.app_constants import AppTableNames
from app.shared.db_constants import AppDbValueConstants


class OrderStatusSeeder(BaseSeeder):
    async def seed(self, session: AsyncSession):
        data = self.get_data()
        await self.load_seeders(
            OrderStatusModel, session, AppTableNames.OrderStatusTableName, data
        )
        updated_data = self.get_updated_data()
        await self.update_seeders(
            OrderStatusModel,
            session,
            AppTableNames.OrderStatusTableName,
            "value",
            updated_data,
            False,
        )

    def get_dev_data(self):
        return [
            OrderStatusModel(
                id=1,
                title="Ожидание создания счета на оплату",
                value=AppDbValueConstants.WAITING_FOR_INVOICE_CREATION_STATUS,
                status=True,
                prev_id=None,
                next_id=None,
                prev_value=None,
                next_value=AppDbValueConstants.WAITING_FOR_PAYMENT_STATUS,
                is_first=True,
                is_last=False,
            ),
            OrderStatusModel(
                id=2,
                title="Ошибка при создании счета на оплату",
                value=AppDbValueConstants.INVOICE_CREATION_ERROR_STATUS,
                status=True,
                prev_id=None,  # Укажите ID предыдущего статуса после добавления
                next_id=None,  # Укажите ID следующего статуса после добавления
                prev_value=AppDbValueConstants.WAITING_FOR_INVOICE_CREATION_STATUS,
                next_value=None,
                is_first=False,
                is_last=False,
            ),
            OrderStatusModel(
                id=3,
                title="Ожидание оплаты",
                value=AppDbValueConstants.WAITING_FOR_PAYMENT_STATUS,
                status=True,
                prev_id=None,  # Укажите ID предыдущего статуса после добавления
                next_id=None,  # Укажите ID следующего статуса после добавления
                prev_value=AppDbValueConstants.WAITING_FOR_INVOICE_CREATION_STATUS,
                next_value=AppDbValueConstants.PAID_WAITING_FOR_BOOKING_STATUS,
                is_first=False,
                is_last=False,
            ),
            OrderStatusModel(
                id=4,
                title="Ожидание подтверждения документов оплаты",
                value=AppDbValueConstants.WAITING_FOR_PAYMENT_CONFIRMATION_STATUS,
                status=True,
                prev_id=None,  # Укажите ID предыдущего статуса после добавления
                next_id=None,  # Укажите ID следующего статуса после добавления
                prev_value=AppDbValueConstants.WAITING_FOR_INVOICE_CREATION_STATUS,
                next_value=AppDbValueConstants.PAID_WAITING_FOR_BOOKING_STATUS,
                is_first=False,
                is_last=False,
            ),
            OrderStatusModel(
                id=5,
                title="Отказ в системе оплаты",
                value=AppDbValueConstants.PAYMENT_REJECTED_STATUS,
                status=True,
                prev_id=None,  # Укажите ID предыдущего статуса после добавления
                next_id=None,  # Укажите ID следующего статуса после добавления
                prev_value=AppDbValueConstants.WAITING_FOR_PAYMENT_STATUS,
                next_value=None,
                is_first=False,
                is_last=False,
            ),
            OrderStatusModel(
                id=6,
                title="Отказ в подтверждении документов оплаты",
                value=AppDbValueConstants.PAYMENT_CONFIRMATION_REJECTED_STATUS,
                status=True,
                prev_id=None,  # Укажите ID предыдущего статуса после добавления
                next_id=None,  # Укажите ID следующего статуса после добавления
                prev_value=AppDbValueConstants.WAITING_FOR_PAYMENT_CONFIRMATION_STATUS,
                next_value=None,
                is_first=False,
                is_last=False,
            ),
            OrderStatusModel(
                id=7,
                title="Оплачено. Ожидает бронирования",
                value=AppDbValueConstants.PAID_WAITING_FOR_BOOKING_STATUS,
                status=True,
                prev_id=None,  # Укажите ID предыдущего статуса после добавления
                next_id=None,  # Укажите ID следующего статуса после добавления
                prev_value=AppDbValueConstants.WAITING_FOR_PAYMENT_STATUS,
                next_value=AppDbValueConstants.IN_PROGRESS_STATUS,
                is_first=False,
                is_last=False,
            ),
            OrderStatusModel(
                id=8,
                title="Заказ выполняется",
                value=AppDbValueConstants.IN_PROGRESS_STATUS,
                status=True,
                prev_id=None,  # Укажите ID предыдущего статуса после добавления
                next_id=None,  # Укажите ID следующего статуса после добавления
                prev_value=AppDbValueConstants.PAID_WAITING_FOR_BOOKING_STATUS,
                next_value=AppDbValueConstants.COMPLETED_STATUS,
                is_first=False,
                is_last=False,
            ),
            OrderStatusModel(
                id=9,
                title="Успешно завершен",
                value=AppDbValueConstants.COMPLETED_STATUS,
                status=True,
                prev_id=None,  # Укажите ID предыдущего статуса после добавления
                next_id=None,
                prev_value=AppDbValueConstants.IN_PROGRESS_STATUS,
                next_value=None,
                is_first=False,
                is_last=True,
            ),
            OrderStatusModel(
                id=10,
                title="Отклонен",
                value=AppDbValueConstants.DECLINED_STATUS,
                status=True,
                prev_id=None,
                next_id=None,
                prev_value=None,
                next_value=None,
                is_first=False,
                is_last=True,
            ),
        ]

    def get_prod_data(self):
        return self.get_dev_data()

    def get_dev_updated_data(self) -> list:
        return [
            OrderStatusModel(
                value=AppDbValueConstants.WAITING_FOR_INVOICE_CREATION_STATUS,
                prev_id=None,
                next_id=2,
            ),
            OrderStatusModel(
                value=AppDbValueConstants.INVOICE_CREATION_ERROR_STATUS,
                prev_id=1,
                next_id=None,
            ),
            OrderStatusModel(
                value=AppDbValueConstants.WAITING_FOR_PAYMENT_STATUS,
                prev_id=1,
                next_id=7,
            ),
            OrderStatusModel(
                value=AppDbValueConstants.WAITING_FOR_PAYMENT_CONFIRMATION_STATUS,
                prev_id=1,
                next_id=7,
            ),
            OrderStatusModel(
                value=AppDbValueConstants.PAYMENT_REJECTED_STATUS,
                prev_id=3,
                next_id=None,
            ),
            OrderStatusModel(
                value=AppDbValueConstants.PAYMENT_CONFIRMATION_REJECTED_STATUS,
                prev_id=4,
                next_id=None,
            ),
            OrderStatusModel(
                value=AppDbValueConstants.PAID_WAITING_FOR_BOOKING_STATUS,
                prev_id=3,
                next_id=8,
            ),
            OrderStatusModel(
                value=AppDbValueConstants.IN_PROGRESS_STATUS,
                prev_id=7,
                next_id=9,
            ),
            OrderStatusModel(
                value=AppDbValueConstants.COMPLETED_STATUS,
                prev_id=8,
                next_id=None,
            ),
            OrderStatusModel(
                value=AppDbValueConstants.DECLINED_STATUS,
                prev_id=None,
                next_id=None,
            ),
        ]

    def get_prod_updated_data(self):
        return self.get_dev_updated_data()
