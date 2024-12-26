from sqlalchemy.orm import Mapped

from app.infrastructure.database import Base
from app.shared.app_constants import AppTableNames
from app.shared.db_constants import DbColumnConstants


class WorkshopScheduleModel(Base):
    __tablename__ = AppTableNames.WorkshopScheduleTableName

    # ID
    id: Mapped[DbColumnConstants.ID]
    # ForeignKey для workshop_id
    workshop_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.WorkshopTableName,
            ondelete="SET NULL",
            onupdate="CASCADE",
        )
    ]
    # Поля для SAP ID
    workshop_sap_id: Mapped[DbColumnConstants.StandardVarcharIndex]
    # Даты начала и окончания
    date_start: Mapped[DbColumnConstants.StandardDate]
    date_end: Mapped[DbColumnConstants.StandardDate]
    # Время начала и окончания
    start_at: Mapped[DbColumnConstants.StandardTime]
    end_at: Mapped[DbColumnConstants.StandardTime]
    # Сервисные настройки
    car_service_min: Mapped[DbColumnConstants.StandardInteger]
    break_between_service_min: Mapped[DbColumnConstants.StandardInteger]
    machine_at_one_time: Mapped[DbColumnConstants.StandardInteger]
    can_earlier_come: Mapped[DbColumnConstants.StandardIntegerDefaultZero]
    can_late_come: Mapped[DbColumnConstants.StandardIntegerDefaultZero]
    # Статус активности
    is_active: Mapped[DbColumnConstants.StandardBooleanTrue]
    # Таймстампы создания и обновления
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
