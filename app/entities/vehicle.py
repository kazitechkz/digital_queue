from typing import List

from sqlalchemy.orm import Mapped

from app.infrastructure.database import Base
from app.shared.app_constants import AppTableNames, AppModelNames
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants


class VehicleModel(Base):
    __tablename__ = AppTableNames.VehicleTableName
    id: Mapped[DbColumnConstants.ID]
    category_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            table_name=AppTableNames.VehicleCategoryTableName,
            ondelete="set null",
            onupdate="cascade",
        )
    ]
    color_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            table_name=AppTableNames.VehicleColorTableName,
            ondelete="set null",
            onupdate="cascade",
        )
    ]

    owner_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            table_name=AppTableNames.UserTableName,
            ondelete="set null",
            onupdate="cascade",
        )
    ]
    organization_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            table_name=AppTableNames.OrganizationTableName,
            ondelete="set null",
            onupdate="cascade",
        )
    ]
    file_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.FileTableName, onupdate="set null", ondelete="cascade"
        )
    ]
    registration_number: Mapped[DbColumnConstants.StandardVarchar]
    car_model: Mapped[DbColumnConstants.StandardVarchar]
    is_trailer: Mapped[DbColumnConstants.StandardBooleanFalse]
    vehicle_info: Mapped[DbColumnConstants.StandardNullableText]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    # Relations

    file: Mapped[AppModelNames.FileModelName] = DbRelationshipConstants.many_to_one(
        target=AppModelNames.FileModelName,
        back_populates="vehicles",
        foreign_keys=f"{AppModelNames.VehicleModelName}.file_id"
    )
    color: Mapped[AppModelNames.VehicleColorModelName] = DbRelationshipConstants.many_to_one(
        target=AppModelNames.VehicleColorModelName,
        back_populates="vehicles",
        foreign_keys=f"{AppModelNames.VehicleModelName}.color_id"
    )
    category: Mapped[AppModelNames.VehicleCategoryModelName] = DbRelationshipConstants.many_to_one(
        target=AppModelNames.VehicleCategoryModelName,
        back_populates="vehicles",
        foreign_keys=f"{AppModelNames.VehicleModelName}.category_id"
    )
    owner: Mapped[AppModelNames.UserModelName] = DbRelationshipConstants.many_to_one(
        target=AppModelNames.UserModelName,
        back_populates="vehicles",
        foreign_keys=f"{AppModelNames.VehicleModelName}.owner_id"
    )
    organization: Mapped[AppModelNames.OrganizationModelName] = DbRelationshipConstants.many_to_one(
        target=AppModelNames.OrganizationModelName,
        back_populates="vehicles",
        foreign_keys=f"{AppModelNames.VehicleModelName}.organization_id"
    )
    act_weights_vehicle: Mapped[List[AppModelNames.ActWeightModelName]] = DbRelationshipConstants.one_to_many(
        target=AppModelNames.ActWeightModelName,
        back_populates="vehicle",
        foreign_keys=f"{AppModelNames.ActWeightModelName}.vehicle_id"
    )
    act_weights_trailer: Mapped[List[AppModelNames.ActWeightModelName]] = DbRelationshipConstants.one_to_many(
        target=AppModelNames.ActWeightModelName,
        back_populates="trailer",
        foreign_keys=f"{AppModelNames.ActWeightModelName}.trailer_id"
    )

    base_weights:Mapped[List[AppModelNames.BaseWeightModelName]] = DbRelationshipConstants.one_to_many(
        target=AppModelNames.BaseWeightModelName,
        back_populates="vehicle",
        foreign_keys=f"{AppModelNames.BaseWeightModelName}.vehicle_id"
    )
    vehicle_schedules: Mapped[List[AppModelNames.ScheduleModelName]] = DbRelationshipConstants.one_to_many(
        target=AppModelNames.ScheduleModelName,
        back_populates="vehicle",
        foreign_keys=f"{AppModelNames.ScheduleModelName}.vehicle_id"
    )
    trailer_schedules: Mapped[List[AppModelNames.ScheduleModelName]] = DbRelationshipConstants.one_to_many(
        target=AppModelNames.ScheduleModelName,
        back_populates="trailer",
        foreign_keys=f"{AppModelNames.ScheduleModelName}.trailer_id"
    )
    verified_vehicles: Mapped[
        List[AppModelNames.VerifiedVehicleModelName]] = DbRelationshipConstants.one_to_many(
        target=AppModelNames.VerifiedVehicleModelName,
        back_populates="vehicle",
        foreign_keys=f"{AppModelNames.VerifiedVehicleModelName}.vehicle_id"
    )

