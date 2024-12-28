from typing import Optional

from sqlalchemy.orm import Mapped

from app.infrastructure.database import Base
from app.shared.app_constants import AppTableNames, AppModelNames
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants


class OperationModel(Base):
    __tablename__ = AppTableNames.OperationTableName
    # Уникальный идентификатор
    id: Mapped[DbColumnConstants.ID]
    # Название операции
    title: Mapped[DbColumnConstants.StandardVarchar]
    # Уникальное значение операции
    value: Mapped[DbColumnConstants.StandardUniqueValue]
    # Роль
    role_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.RoleTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    role_value: Mapped[DbColumnConstants.StandardNullableVarcharIndex]
    role_keycloak_value: Mapped[DbColumnConstants.StandardNullableVarcharIndex]

    # Флаги положения операции
    is_first: Mapped[DbColumnConstants.StandardBooleanFalse]
    is_last: Mapped[DbColumnConstants.StandardBooleanFalse]

    # Ссылки на предыдущую и следующую операции
    prev_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.OperationTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    next_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.OperationTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    prev_value: Mapped[DbColumnConstants.StandardNullableVarcharIndex]
    next_value: Mapped[DbColumnConstants.StandardNullableVarcharIndex]
    # Возможность отмены
    can_cancel: Mapped[DbColumnConstants.StandardBooleanFalse]
    is_active: Mapped[DbColumnConstants.StandardBooleanTrue]
    # Таймстампы создания и обновления
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    prev_operation: Mapped[Optional[AppModelNames.OperationModelName]] = DbRelationshipConstants.self_referential(
        target=AppModelNames.OperationModelName,
        foreign_keys=f"{AppModelNames.OperationModelName}.prev_id",
        remote_side=f"{AppModelNames.OperationModelName}.id",
    )

    next_operation: Mapped[Optional[AppModelNames.OperationModelName]] = DbRelationshipConstants.self_referential(
        target=AppModelNames.OperationModelName,
        foreign_keys=f"{AppModelNames.OperationModelName}.next_id",
        remote_side=f"{AppModelNames.OperationModelName}.id",
    )