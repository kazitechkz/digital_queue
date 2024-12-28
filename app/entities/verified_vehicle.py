from sqlalchemy.orm import Mapped

from app.infrastructure.database import Base
from app.shared.app_constants import AppTableNames, AppModelNames
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants


class VerifiedVehicleModel(Base):
    __tablename__ = AppTableNames.VerifiedVehicleTableName
    # ID
    id: Mapped[DbColumnConstants.ID]
    vehicle_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            table_name=AppTableNames.VehicleTableName,
            onupdate="cascade",
            ondelete="set null",
        )
    ]
    car_number: Mapped[DbColumnConstants.StandardNullableVarcharIndex]
    verified_at: Mapped[DbColumnConstants.StandardNullableDateTime]
    will_act_at: Mapped[DbColumnConstants.StandardNullableDateTime]
    is_waiting_for_response: Mapped[DbColumnConstants.StandardBooleanTrue]
    is_verified: Mapped[DbColumnConstants.StandardBooleanNullable]
    is_rejected: Mapped[DbColumnConstants.StandardBooleanNullable]
    description: Mapped[DbColumnConstants.StandardNullableText]
    response: Mapped[DbColumnConstants.StandardNullableText]
    verified_by: Mapped[DbColumnConstants.StandardNullableVarcharIndex]
    verified_by_sid: Mapped[DbColumnConstants.StandardNullableVarcharIndex]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
    # Relations
    vehicle: Mapped[AppModelNames.UserModelName] = DbRelationshipConstants.many_to_one(
        target=AppModelNames.VehicleModelName,
        back_populates="verified_vehicles",
        foreign_keys=f"{AppModelNames.VerifiedVehicleModelName}.vehicle_id"
    )