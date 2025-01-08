from typing import List

from sqlalchemy.orm import Mapped

from app.infrastructure.database import Base
from app.shared.app_constants import AppModelNames, AppTableNames
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants


class OrganizationModel(Base):
    __tablename__ = AppTableNames.OrganizationTableName
    id: Mapped[DbColumnConstants.ID]
    file_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.FileTableName, onupdate="set null", ondelete="cascade"
        )
    ]
    full_name: Mapped[DbColumnConstants.StandardText]
    short_name: Mapped[DbColumnConstants.StandardText]
    bin: Mapped[DbColumnConstants.StandardUniqueBIN]
    bik: Mapped[DbColumnConstants.StandardNullableVarchar]
    kbe: Mapped[DbColumnConstants.StandardNullableVarchar]
    email: Mapped[DbColumnConstants.StandardUniqueEmail]
    phone: Mapped[DbColumnConstants.StandardUniquePhone]
    address: Mapped[DbColumnConstants.StandardNullableText]
    status: Mapped[DbColumnConstants.StandardBooleanTrue]
    is_verified: Mapped[DbColumnConstants.StandardBooleanNullable]
    owner_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            table_name=AppTableNames.UserTableName,
            onupdate="cascade",
            ondelete="set null",
        )
    ]
    type_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            table_name=AppTableNames.OrganizationTypeTableName,
            onupdate="cascade",
            ondelete="set null",
        )
    ]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    # Relations
    employee_requests: Mapped[List[AppModelNames.EmployeeRequestModelName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppModelNames.EmployeeRequestModelName,
            back_populates="organization",
        )
    )
    orders: Mapped[List[AppModelNames.OrderModelName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppModelNames.OrderModelName,
            back_populates="organization",
            foreign_keys=f"{AppModelNames.OrderModelName}.organization_id",
        )
    )
    file: Mapped[AppModelNames.FileModelName] = DbRelationshipConstants.many_to_one(
        target=AppModelNames.FileModelName,
        back_populates="organizations",
        foreign_keys=f"{AppModelNames.OrganizationModelName}.file_id",
    )
    owner: Mapped[AppModelNames.UserModelName] = DbRelationshipConstants.many_to_one(
        target=AppModelNames.UserModelName,
        back_populates="organizations",
        foreign_keys=f"{AppModelNames.OrganizationModelName}.owner_id",
    )
    type: Mapped[AppModelNames.OrganizationTypeModelName] = (
        DbRelationshipConstants.many_to_one(
            target=AppModelNames.OrganizationTypeModelName,
            back_populates="organizations",
            foreign_keys=f"{AppModelNames.OrganizationModelName}.type_id",
        )
    )
    organization_employees: Mapped[
        List[AppModelNames.OrganizationEmployeeModelName]
    ] = DbRelationshipConstants.one_to_many(
        target=AppModelNames.OrganizationEmployeeModelName,
        back_populates="organization",
        foreign_keys=f"{AppModelNames.OrganizationEmployeeModelName}.organization_id",
    )
    schedules: Mapped[List[AppModelNames.ScheduleModelName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppModelNames.ScheduleModelName,
            back_populates="organization",
            foreign_keys=f"{AppModelNames.ScheduleModelName}.organization_id",
        )
    )
    vehicles: Mapped[List[AppModelNames.VehicleModelName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppModelNames.VehicleModelName,
            back_populates="organization",
            foreign_keys=f"{AppModelNames.VehicleModelName}.organization_id",
        )
    )
