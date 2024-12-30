from typing import List

from sqlalchemy.orm import Mapped, relationship

from app.infrastructure.database import Base
from app.shared.app_constants import AppModelNames, AppTableNames
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants


class UserTypeModel(Base):
    __tablename__ = AppTableNames.UserTypeTableName
    id: Mapped[DbColumnConstants.ID]
    title: Mapped[DbColumnConstants.StandardVarchar]
    value: Mapped[DbColumnConstants.StandardUniqueValue]
    keycloak_id: Mapped[DbColumnConstants.StandardNullableVarchar]
    keycloak_value: Mapped[DbColumnConstants.StandardVarchar]
    is_active: Mapped[DbColumnConstants.StandardBooleanTrue]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    # Relations
    users: Mapped[List[AppModelNames.UserModelName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppModelNames.UserModelName,
            back_populates="user_type",
            foreign_keys=f"{AppModelNames.UserModelName}.type_id",
        )
    )
