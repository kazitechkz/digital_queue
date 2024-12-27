import logging
from abc import ABC, abstractmethod

from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.config import app_config

logger = logging.getLogger(__name__)


class BaseSeeder(ABC):
    """Базовый класс для всех сидеров."""

    def __init__(self):
        self.environment = (
            app_config.app_status
        )  # Получение текущего окружения (prod/dev)
        self.db_type = app_config.app_database

    @abstractmethod
    async def seed(self, session: AsyncSession):
        """Метод для заполнения базы данных."""
        pass

    def get_data(self):
        """Загрузка данных в зависимости от окружения."""
        if self.environment == "production":
            return self.get_prod_data()
        else:
            return self.get_dev_data()

    def get_updated_data(self):
        """Загрузка данных в зависимости от окружения."""
        if self.environment == "production":
            return self.get_prod_updated_data()
        else:
            return self.get_dev_updated_data()

    @abstractmethod
    def get_dev_data(self):
        """Возвращает данные для разработки."""
        pass

    @abstractmethod
    def get_prod_data(self):
        """Возвращает данные для продакшена."""
        pass

    @abstractmethod
    def get_dev_updated_data(self):
        """Возвращает данные для разработки."""
        pass

    @abstractmethod
    def get_prod_updated_data(self):
        """Возвращает данные для продакшена."""
        pass

    async def reset_sequence(self, session: AsyncSession, table_name: str):

        if self.db_type.startswith("postgresql"):
            await session.execute(
                text(
                    f"""
                       DO $$
                       BEGIN
                           IF EXISTS (SELECT 1 FROM {table_name}) THEN
                               PERFORM setval(pg_get_serial_sequence('{table_name}', 'id'), MAX(id)) FROM {table_name};
                           ELSE
                               PERFORM setval(pg_get_serial_sequence('{table_name}', 'id'), 1, false);
                           END IF;
                       END
                       $$;
                   """
                )
            )
            logger.info(f"Последовательность для таблицы {table_name} сброшена.")

    async def load_seeders(
        self, BaseModel, session, table_name: str, ready_data: list = None
    ):
        # Проверяем, есть ли данные в таблице
        count_query = select(func.count()).select_from(BaseModel)
        total_items = await session.scalar(count_query)

        if total_items > 0:
            logger.info(
                f"Таблица {table_name} уже содержит данные ({total_items} записей)."
            )
            return

        # Добавляем данные, если они переданы
        if ready_data:
            session.add_all(ready_data)
            await session.commit()

            # Сбрасываем последовательность для PostgreSQL
            await self.reset_sequence(session, table_name)

            print(
                f"Данные успешно добавлены в таблицу {table_name} ({len(ready_data)} записей)."
            )

    async def update_seeders(
        self,
        BaseModel,
        session: AsyncSession,
        table_name: str,
        identification: str,
        update_data: list,
        add_if_not_exists: bool = False,
    ):
        """
        Обновление данных в таблице.

        Args:
            BaseModel: SQLAlchemy модель таблицы.
            session: Активная асинхронная сессия.
            table_name: Имя таблицы (для логирования).
            identification: Поле для идентификации записи (например, 'id').
            update_data: Список записей для обновления/добавления.
            add_if_not_exists: Если True, добавляет новые записи, если их не существует.
        """
        if not update_data:
            logger.info(f"Нет данных для обновления/добавления в таблицу {table_name}.")
            return

        for record in update_data:
            # Используем getattr для безопасного доступа к атрибутам
            identifier = getattr(record, identification, None)
            print(identifier)
            if identifier is None:
                raise ValueError(
                    f"Каждая запись должна содержать поле '{identification}' для идентификации."
                )

            # Поиск записи по идентификатору (не через get(), так как поле не является ключом)
            stmt = select(BaseModel).where(
                getattr(BaseModel, identification) == identifier
            )
            result = await session.execute(stmt)
            existing_record = result.scalar_one_or_none()

            if existing_record:
                # Обновляем поля записи
                for key, value in record.items():
                    if key != identification:  # Поле идентификации не обновляем
                        setattr(existing_record, key, value)
                logger.info(
                    f"Обновлена запись с {identification}={identifier} в таблице {table_name}."
                )
            elif add_if_not_exists:
                # Добавляем новую запись
                new_record = BaseModel(**record)
                session.add(new_record)
                logger.info(
                    f"Добавлена новая запись с {identification}={identifier} в таблицу {table_name}."
                )

        await session.commit()
        logger.info(f"Данные успешно обновлены/добавлены в таблицу {table_name}.")
