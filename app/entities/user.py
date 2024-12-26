from typing import Optional

from sqlalchemy.orm import Mapped, relationship

from app.infrastructure.database import Base
from app.shared.app_constants import AppModelNames, AppTableNames
from app.shared.db_constants import DbColumnConstants


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
