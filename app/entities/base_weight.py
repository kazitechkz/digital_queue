from sqlalchemy.orm import Mapped

from app.infrastructure.database import Base
from app.shared.app_constants import AppModelNames, AppTableNames
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants


class BaseWeightModel(Base):
    __tablename__ = AppTableNames.BaseWeightTableName

    # Уникальный идентификатор
    id: Mapped[DbColumnConstants.ID]

    # Идентификатор транспортного средства
    vehicle_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.VehicleTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]

    # Информация о транспортном средстве
    car_number: Mapped[DbColumnConstants.StandardVarcharIndex]

    # Вес транспортного средства (тара)
    vehicle_tara_kg: Mapped[DbColumnConstants.StandardInteger]

    # Время измерения веса и его действие
    measured_at: Mapped[DbColumnConstants.StandardDateTime]
    measured_to: Mapped[DbColumnConstants.StandardDateTime]

    # Таймстампы создания и обновления
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    # Relations
    vehicle: Mapped[AppModelNames.VehicleModelName] = (
        DbRelationshipConstants.many_to_one(
            target=AppModelNames.VehicleModelName,
            back_populates="base_weights",
            foreign_keys=f"{AppModelNames.BaseWeightModelName}.vehicle_id",
        )
    )
