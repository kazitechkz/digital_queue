from typing import Optional, List

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
    role: Mapped[Optional[AppModelNames.RoleModelName]] = relationship(
        back_populates="users"
    )
    user_type: Mapped[Optional[AppModelNames.UserTypeModelName]] = relationship(
        back_populates="users"
    )

    #Relations
    act_weights: Mapped[List[AppModelNames.ActWeightModelName]] = DbRelationshipConstants.one_to_many(
        target=AppModelNames.ActWeightModelName,
        back_populates="responsible",
    )

    sent_employee_requests: Mapped[List[AppModelNames.EmployeeRequestModelName]] = DbRelationshipConstants.one_to_many(
        target=AppModelNames.EmployeeRequestModelName,
        back_populates="owner",
        foreign_keys=f"{AppModelNames.EmployeeRequestModelName}.owner_id"
    )

    received_employee_requests: Mapped[List[AppModelNames.EmployeeRequestModelName]] = DbRelationshipConstants.one_to_many(
        target=AppModelNames.EmployeeRequestModelName,
        back_populates="employee",
        foreign_keys=f"{AppModelNames.EmployeeRequestModelName}.employee_id"
    )
    orders: Mapped[List[AppModelNames.OrderModelName]] = DbRelationshipConstants.one_to_many(
        target=AppModelNames.OrderModelName,
        back_populates="owner",
        foreign_keys=f"{AppModelNames.OrderModelName}.owner_id"
    )
    cancelled_orders: Mapped[List[AppModelNames.OrderModelName]] = DbRelationshipConstants.one_to_many(
        target=AppModelNames.OrderModelName,
        back_populates="canceled_by",
        foreign_keys=f"{AppModelNames.OrderModelName}.canceled_by_user"
    )
    checked_payment_orders: Mapped[List[AppModelNames.OrderModelName]] = DbRelationshipConstants.one_to_many(
        target=AppModelNames.OrderModelName,
        back_populates="checked_payment_by",
        foreign_keys=f"{AppModelNames.OrderModelName}.checked_payment_by_id"
    )
    organizations:Mapped[List[AppModelNames.OrganizationModelName]] = DbRelationshipConstants.one_to_many(
        target=AppModelNames.OrganizationModelName,
        back_populates="owner",
        foreign_keys=f"{AppModelNames.OrganizationModelName}.owner_id"
    )

