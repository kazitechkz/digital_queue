from sqlalchemy.orm import Mapped

from app.infrastructure.database import Base
from app.shared.app_constants import AppTableNames
from app.shared.db_constants import DbColumnConstants


class PaymentReturnModel(Base):
    __tablename__ = AppTableNames.PaymentReturnTableName
    id: Mapped[DbColumnConstants.ID]
    amount: Mapped[DbColumnConstants.StandardPrice]
    order_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.OrderTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    zakaz: Mapped[DbColumnConstants.StandardNullableVarcharIndex]
    owner_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.UserTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    owner_name: Mapped[DbColumnConstants.StandardVarcharIndex]
    owner_iin: Mapped[DbColumnConstants.StandardVarcharIndex]
    owner_sid: Mapped[DbColumnConstants.StandardNullableVarcharIndex]
    status: Mapped[DbColumnConstants.StandardNullableInteger]
    comment: Mapped[DbColumnConstants.StandardNullableVarchar]
    decided_by_name: Mapped[DbColumnConstants.StandardNullableVarchar]
    decided_by_sid: Mapped[DbColumnConstants.StandardNullableVarchar]
    decided_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.UserTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    cancel_reason: Mapped[DbColumnConstants.StandardNullableText]
    # Таймстампы создания и обновления
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]