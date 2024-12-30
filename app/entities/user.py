from typing import List, Optional

from sqlalchemy.orm import Mapped, relationship

from app.infrastructure.database import Base
from app.shared.app_constants import AppModelNames, AppTableNames
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants


class UserModel(Base):
    __tablename__ = AppTableNames.UserTableName
    id: Mapped[DbColumnConstants.ID]
    sid: Mapped[DbColumnConstants.StandardUniqueValue]
    iin: Mapped[DbColumnConstants.StandardUniqueIIN]
    role_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            table_name=AppTableNames.RoleTableName,
            onupdate="cascade",
            ondelete="set null",
        )
    ]
    type_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            table_name=AppTableNames.UserTypeTableName,
            onupdate="cascade",
            ondelete="set null",
        )
    ]
    file_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.FileTableName, onupdate="set null", ondelete="cascade"
        )
    ]
    name: Mapped[DbColumnConstants.StandardVarchar]
    given_name: Mapped[DbColumnConstants.StandardNullableVarchar]
    family_name: Mapped[DbColumnConstants.StandardNullableVarchar]
    preferred_username: Mapped[DbColumnConstants.StandardUniqueValue]
    email: Mapped[DbColumnConstants.StandardEmail]
    email_verified: Mapped[DbColumnConstants.StandardBooleanFalse]
    phone: Mapped[DbColumnConstants.StandardNullableVarchar]
    phone_verified: Mapped[DbColumnConstants.StandardBooleanFalse]
    tabn: Mapped[DbColumnConstants.StandardNullableVarchar]
    status: Mapped[DbColumnConstants.StandardBooleanTrue]
    password_hash: Mapped[DbColumnConstants.StandardNullableText]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    # Relations
    role: Mapped[AppModelNames.RoleModelName] = DbRelationshipConstants.many_to_one(
        target=AppModelNames.RoleModelName,
        back_populates="users",
        foreign_keys=f"{AppModelNames.UserModelName}.role_id",
    )
    user_type: Mapped[AppModelNames.UserTypeModelName] = (
        DbRelationshipConstants.many_to_one(
            target=AppModelNames.UserTypeModelName,
            back_populates="users",
            foreign_keys=f"{AppModelNames.UserModelName}.type_id",
        )
    )
    file: Mapped[AppModelNames.FileModelName] = DbRelationshipConstants.many_to_one(
        target=AppModelNames.FileModelName,
        back_populates="users",
        foreign_keys=f"{AppModelNames.UserModelName}.file_id",
    )

    # Relations
    act_weights: Mapped[List[AppModelNames.ActWeightModelName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppModelNames.ActWeightModelName,
            back_populates="responsible",
        )
    )

    sent_employee_requests: Mapped[List[AppModelNames.EmployeeRequestModelName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppModelNames.EmployeeRequestModelName,
            back_populates="owner",
            foreign_keys=f"{AppModelNames.EmployeeRequestModelName}.owner_id",
        )
    )

    received_employee_requests: Mapped[List[AppModelNames.EmployeeRequestModelName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppModelNames.EmployeeRequestModelName,
            back_populates="employee",
            foreign_keys=f"{AppModelNames.EmployeeRequestModelName}.employee_id",
        )
    )
    orders: Mapped[List[AppModelNames.OrderModelName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppModelNames.OrderModelName,
            back_populates="owner",
            foreign_keys=f"{AppModelNames.OrderModelName}.owner_id",
        )
    )
    cancelled_orders: Mapped[List[AppModelNames.OrderModelName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppModelNames.OrderModelName,
            back_populates="canceled_by",
            foreign_keys=f"{AppModelNames.OrderModelName}.canceled_by_user",
        )
    )
    checked_payment_orders: Mapped[List[AppModelNames.OrderModelName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppModelNames.OrderModelName,
            back_populates="checked_payment_by",
            foreign_keys=f"{AppModelNames.OrderModelName}.checked_payment_by_id",
        )
    )
    organizations: Mapped[List[AppModelNames.OrganizationModelName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppModelNames.OrganizationModelName,
            back_populates="owner",
            foreign_keys=f"{AppModelNames.OrganizationModelName}.owner_id",
        )
    )
    organization_employees: Mapped[
        List[AppModelNames.OrganizationEmployeeModelName]
    ] = DbRelationshipConstants.one_to_many(
        target=AppModelNames.OrganizationEmployeeModelName,
        back_populates="employee",
        foreign_keys=f"{AppModelNames.OrganizationEmployeeModelName}.employee_id",
    )
    payment_documents: Mapped[List[AppModelNames.PaymentDocumentModelName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppModelNames.PaymentDocumentModelName,
            back_populates="checked_by_user",
            foreign_keys=f"{AppModelNames.PaymentDocumentModelName}.checked_by",
        )
    )
    payment_returns: Mapped[List[AppModelNames.PaymentReturnModelName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppModelNames.PaymentReturnModelName,
            back_populates="owner",
            foreign_keys=f"{AppModelNames.PaymentReturnModelName}.owner_id",
        )
    )
    decided_payment_returns: Mapped[List[AppModelNames.PaymentReturnModelName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppModelNames.PaymentReturnModelName,
            back_populates="decided",
            foreign_keys=f"{AppModelNames.PaymentReturnModelName}.decided_id",
        )
    )
    owner_schedules: Mapped[List[AppModelNames.ScheduleModelName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppModelNames.ScheduleModelName,
            back_populates="owner",
            foreign_keys=f"{AppModelNames.ScheduleModelName}.owner_id",
        )
    )
    driver_schedules: Mapped[List[AppModelNames.ScheduleModelName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppModelNames.ScheduleModelName,
            back_populates="driver",
            foreign_keys=f"{AppModelNames.ScheduleModelName}.driver_id",
        )
    )
    responsible_for_schedules: Mapped[List[AppModelNames.ScheduleModelName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppModelNames.ScheduleModelName,
            back_populates="responsible",
            foreign_keys=f"{AppModelNames.ScheduleModelName}.responsible_id",
        )
    )
    canceled_schedules: Mapped[List[AppModelNames.ScheduleModelName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppModelNames.ScheduleModelName,
            back_populates="canceled_by_user",
            foreign_keys=f"{AppModelNames.ScheduleModelName}.canceled_by",
        )
    )
    histories: Mapped[List[AppModelNames.ScheduleHistoryModelName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppModelNames.ScheduleHistoryModelName,
            back_populates="responsible",
            foreign_keys=f"{AppModelNames.ScheduleHistoryModelName}.responsible_id",
        )
    )
    vehicles: Mapped[List[AppModelNames.VehicleModelName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppModelNames.VehicleModelName,
            back_populates="owner",
            foreign_keys=f"{AppModelNames.VehicleModelName}.owner_id",
        )
    )
    verified_users: Mapped[List[AppModelNames.VerifiedUserModelName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppModelNames.VerifiedUserModelName,
            back_populates="user",
            foreign_keys=f"{AppModelNames.VerifiedUserModelName}.user_id",
        )
    )
