from sqlalchemy.orm import Mapped

from app.infrastructure.database import Base
from app.shared.app_constants import AppModelNames, AppTableNames
from app.shared.db_constants import (DbColumnConstants, DbModelValue,
                                     DbRelationshipConstants)


class ScheduleModel(Base):
    __tablename__ = AppTableNames.ScheduleTableName
    # Уникальный идентификатор
    id: Mapped[DbColumnConstants.ID]
    # Заказ
    order_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.OrderTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    zakaz: Mapped[DbColumnConstants.StandardNullableVarcharIndex]
    # Владелец
    owner_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.UserTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    owner_name: Mapped[DbColumnConstants.StandardVarcharIndex]
    owner_iin: Mapped[DbColumnConstants.StandardVarcharIndex]
    owner_sid: Mapped[DbColumnConstants.StandardNullableVarcharIndex]

    # Водитель
    driver_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.UserTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    driver_name: Mapped[DbColumnConstants.StandardVarchar]
    driver_iin: Mapped[DbColumnConstants.StandardVarchar]
    driver_sid: Mapped[DbColumnConstants.StandardNullableVarcharIndex]

    # Организация
    organization_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.OrganizationTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    organization_full_name: Mapped[DbColumnConstants.StandardNullableVarchar]
    organization_bin: Mapped[DbColumnConstants.StandardNullableVarchar]

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
    car_number: Mapped[DbColumnConstants.StandardNullableVarcharIndex]
    # Связанные операции и расписания
    workshop_schedule_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.WorkshopScheduleTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    current_operation_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.OperationTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    current_operation_name: Mapped[DbColumnConstants.StandardNullableVarcharIndex]
    current_operation_value: Mapped[DbColumnConstants.StandardNullableVarcharIndex]
    # Временные данные
    start_at: Mapped[DbColumnConstants.StandardDateTime]
    end_at: Mapped[DbColumnConstants.StandardDateTime]
    rescheduled_start_at: Mapped[DbColumnConstants.StandardNullableDateTime]
    rescheduled_end_at: Mapped[DbColumnConstants.StandardNullableDateTime]
    # Весовые данные
    loading_volume: Mapped[DbColumnConstants.StandardPrice]
    loading_volume_kg: Mapped[
        DbColumnConstants.StandardComputedInteger(
            table_exp=DbModelValue().to_kg(column_name="loading_volume")
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
    # Ответственные лица
    responsible_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.UserTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    responsible_name: Mapped[DbColumnConstants.StandardNullableVarchar]
    # Статусы
    is_active: Mapped[DbColumnConstants.StandardBooleanTrue]
    is_used: Mapped[DbColumnConstants.StandardBooleanFalse]
    is_canceled: Mapped[DbColumnConstants.StandardBooleanFalse]
    is_executed: Mapped[DbColumnConstants.StandardBooleanFalse]
    executed_at: Mapped[DbColumnConstants.StandardNullableDateTime]

    # Отмена
    canceled_by: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.UserTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    canceled_by_name: Mapped[DbColumnConstants.StandardNullableVarchar]
    canceled_by_sid: Mapped[DbColumnConstants.StandardNullableVarchar]
    cancel_reason: Mapped[DbColumnConstants.StandardNullableText]
    canceled_at: Mapped[DbColumnConstants.StandardNullableDateTime]
    # Таймстампы создания и обновления
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    # Relationships
    order: Mapped[AppModelNames.OrderModelName] = DbRelationshipConstants.many_to_one(
        target=AppModelNames.OrderModelName,
        back_populates="schedules",
        foreign_keys=f"{AppModelNames.ScheduleModelName}.order_id",
    )
    owner: Mapped[AppModelNames.UserModelName] = DbRelationshipConstants.many_to_one(
        target=AppModelNames.UserModelName,
        back_populates="owner_schedules",
        foreign_keys=f"{AppModelNames.ScheduleModelName}.owner_id",
    )
    driver: Mapped[AppModelNames.UserModelName] = DbRelationshipConstants.many_to_one(
        target=AppModelNames.UserModelName,
        back_populates="driver_schedules",
        foreign_keys=f"{AppModelNames.ScheduleModelName}.driver_id",
    )
    organization: Mapped[AppModelNames.OrganizationModelName] = (
        DbRelationshipConstants.many_to_one(
            target=AppModelNames.OrganizationModelName,
            back_populates="schedules",
            foreign_keys=f"{AppModelNames.ScheduleModelName}.organization_id",
        )
    )
    vehicle: Mapped[AppModelNames.VehicleModelName] = (
        DbRelationshipConstants.many_to_one(
            target=AppModelNames.VehicleModelName,
            back_populates="vehicle_schedules",
            foreign_keys=f"{AppModelNames.ScheduleModelName}.vehicle_id",
        )
    )
    trailer: Mapped[AppModelNames.VehicleModelName] = (
        DbRelationshipConstants.many_to_one(
            target=AppModelNames.VehicleModelName,
            back_populates="trailer_schedules",
            foreign_keys=f"{AppModelNames.ScheduleModelName}.trailer_id",
        )
    )
    workshop_schedule: Mapped[AppModelNames.WorkshopScheduleModelName] = (
        DbRelationshipConstants.many_to_one(
            target=AppModelNames.WorkshopScheduleModelName,
            back_populates="schedules",
            foreign_keys=f"{AppModelNames.ScheduleModelName}.workshop_schedule_id",
        )
    )
    current_operation: Mapped[AppModelNames.OperationModelName] = (
        DbRelationshipConstants.many_to_one(
            target=AppModelNames.OperationModelName,
            back_populates="schedules",
            foreign_keys=f"{AppModelNames.ScheduleModelName}.current_operation_id",
        )
    )
    responsible: Mapped[AppModelNames.UserModelName] = (
        DbRelationshipConstants.many_to_one(
            target=AppModelNames.UserModelName,
            back_populates="responsible_for_schedules",
            foreign_keys=f"{AppModelNames.ScheduleModelName}.responsible_id",
        )
    )
    canceled_by_user: Mapped[AppModelNames.UserModelName] = (
        DbRelationshipConstants.many_to_one(
            target=AppModelNames.UserModelName,
            back_populates="canceled_schedules",
            foreign_keys=f"{AppModelNames.ScheduleModelName}.canceled_by",
        )
    )
    histories: Mapped[AppModelNames.ScheduleHistoryModelName] = (
        DbRelationshipConstants.many_to_one(
            target=AppModelNames.ScheduleHistoryModelName,
            back_populates="schedule",
            foreign_keys=f"{AppModelNames.ScheduleHistoryModelName}.schedule_id",
        )
    )
