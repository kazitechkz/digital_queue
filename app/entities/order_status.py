from sqlalchemy.orm import Mapped

from app.infrastructure.database import Base
from app.shared.app_constants import AppTableNames
from app.shared.db_constants import DbColumnConstants


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
    is_first: Mapped[DbColumnConstants.StandardBooleanFalse]
    is_last: Mapped[DbColumnConstants.StandardBooleanFalse]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
