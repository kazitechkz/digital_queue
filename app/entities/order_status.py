from typing import Optional

from sqlalchemy.orm import Mapped

from app.infrastructure.database import Base
from app.shared.app_constants import AppModelNames, AppTableNames
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants


class OrderStatusModel(Base):
    __tablename__ = AppTableNames.OrderStatusTableName
    id: Mapped[DbColumnConstants.ID]
    title: Mapped[DbColumnConstants.StandardVarchar]
    value: Mapped[DbColumnConstants.StandardUniqueValue]
    status: Mapped[DbColumnConstants.StandardBooleanTrue]
    prev_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.OrderStatusTableName, ondelete="set null", onupdate="cascade"
        )
    ]
    next_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.OrderStatusTableName, ondelete="set null", onupdate="cascade"
        )
    ]
    prev_value: Mapped[DbColumnConstants.StandardNullableVarcharIndex]
    next_value: Mapped[DbColumnConstants.StandardNullableVarcharIndex]
    is_first: Mapped[DbColumnConstants.StandardBooleanFalse]
    is_last: Mapped[DbColumnConstants.StandardBooleanFalse]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    prev_order_status: Mapped[Optional[AppModelNames.OrderStatusModelName]] = (
        DbRelationshipConstants.self_referential(
            target=AppModelNames.OrderStatusModelName,
            foreign_keys=f"{AppModelNames.OrderStatusModelName}.prev_id",
            remote_side=f"{AppModelNames.OrderStatusModelName}.id",
        )
    )

    next_order_status: Mapped[Optional[AppModelNames.OrderStatusModelName]] = (
        DbRelationshipConstants.self_referential(
            target=AppModelNames.OrderStatusModelName,
            foreign_keys=f"{AppModelNames.OrderStatusModelName}.next_id",
            remote_side=f"{AppModelNames.OrderStatusModelName}.id",
        )
    )
