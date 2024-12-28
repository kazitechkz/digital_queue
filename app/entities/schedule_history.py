from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped

from app.infrastructure.database import Base
from app.shared.app_constants import AppTableNames, AppModelNames
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants


class ScheduleHistoryModel(Base):
    __tablename__ = AppTableNames.ScheduleHistoryTableName
    # Уникальный идентификатор
    id: Mapped[DbColumnConstants.ID]
    # Связь с расписанием
    schedule_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.ScheduleTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    # Операция
    operation_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.OperationTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
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
    # Статус прохождения
    is_passed: Mapped[DbColumnConstants.StandardBooleanNullable]
    # Временные данные
    start_at: Mapped[DbColumnConstants.StandardNullableDateTime]
    end_at: Mapped[DbColumnConstants.StandardNullableDateTime]
    canceled_at: Mapped[DbColumnConstants.StandardNullableDateTime]
    cancel_reason: Mapped[DbColumnConstants.StandardNullableText]
    # Таймстампы создания и обновления
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    # Отношения
    act_weights: Mapped[AppModelNames.ActWeightModelName] = DbRelationshipConstants.one_to_one(
        target=AppModelNames.ActWeightModelName,
        back_populates="history",
        foreign_keys=f"{AppModelNames.ActWeightModelName}.history_id",
    )
