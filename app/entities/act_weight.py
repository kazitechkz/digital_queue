from sqlalchemy.orm import Mapped

from app.infrastructure.database import Base
from app.shared.app_constants import AppTableNames
from app.shared.db_constants import DbColumnConstants, DbModelValue


class ActWeightModel(Base):
    __tablename__ = AppTableNames.ActWeightTableName

    # Уникальный идентификатор
    id: Mapped[DbColumnConstants.ID]
    # История расписания
    history_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.ScheduleHistoryTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    # Заказ
    order_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.OrderTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    zakaz: Mapped[DbColumnConstants.StandardNullableVarcharIndex]
    # Транспортное средство
    vehicle_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.VehicleTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    vehicle_info: Mapped[DbColumnConstants.StandardText]

    # Прицеп
    trailer_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.VehicleTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    trailer_info: Mapped[DbColumnConstants.StandardNullableText]

    # Ответственное лицо
    responsible_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.UserTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    responsible_name: Mapped[DbColumnConstants.StandardNullableVarchar]
    responsible_iin: Mapped[DbColumnConstants.StandardNullableVarchar]
    # Весовые данные
    asvu_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.ASVUWeightTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    vehicle_tara: Mapped[DbColumnConstants.StandardPrice]
    vehicle_netto: Mapped[DbColumnConstants.StandardPrice]
    vehicle_brutto: Mapped[DbColumnConstants.StandardPrice]
    vehicle_tara_kg: Mapped[
        DbColumnConstants.StandardComputedInteger(
            table_exp=DbModelValue().to_kg(column_name="vehicle_tara")
        )
    ]
    vehicle_netto_kg: Mapped[
        DbColumnConstants.StandardComputedInteger(
            table_exp=DbModelValue().to_kg(column_name="vehicle_netto")
        )
    ]
    vehicle_brutto_kg: Mapped[
        DbColumnConstants.StandardComputedInteger(
            table_exp=DbModelValue().to_kg(column_name="vehicle_brutto")
        )
    ]
    # Дата измерения
    measured_at: Mapped[DbColumnConstants.StandardDateTime]
    # Таймстампы создания и обновления
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
