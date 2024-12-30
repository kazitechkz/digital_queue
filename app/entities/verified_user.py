from sqlalchemy.orm import Mapped

from app.infrastructure.database import Base
from app.shared.app_constants import AppModelNames, AppTableNames
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants


class VerifiedUserModel(Base):
    __tablename__ = AppTableNames.VerifiedUserTableName

    # ID
    id: Mapped[DbColumnConstants.ID]
    user_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            table_name=AppTableNames.UserTableName,
            onupdate="cascade",
            ondelete="set null",
        )
    ]
    iin: Mapped[DbColumnConstants.StandardNullableVarcharIndex]
    sid: Mapped[DbColumnConstants.StandardNullableVarcharIndex]
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
    user: Mapped[AppModelNames.UserModelName] = DbRelationshipConstants.many_to_one(
        target=AppModelNames.UserModelName,
        back_populates="verified_users",
        foreign_keys=f"{AppModelNames.VerifiedUserModelName}.user_id",
    )
