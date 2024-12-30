from typing import List

from sqlalchemy.orm import Mapped

from app.infrastructure.database import Base
from app.shared.app_constants import AppModelNames, AppTableNames
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants


class KaspiPaymentModel(Base):
    __tablename__ = AppTableNames.KaspiPaymentsTableName

    id: Mapped[DbColumnConstants.ID]
    order_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.OrderTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    zakaz: Mapped[DbColumnConstants.StandardVarcharIndex]  # № заказа
    account: Mapped[DbColumnConstants.StandardVarcharIndex]  # Счёт
    txn_id: Mapped[DbColumnConstants.StandardNullableVarcharIndex]  # ID транзакции
    txn_check_id: Mapped[
        DbColumnConstants.StandardNullableVarcharIndex
    ]  # ID проверки транзакции
    txn_pay_id: Mapped[
        DbColumnConstants.StandardNullableVarcharIndex
    ]  # ID оплаты транзакции
    txn_date: Mapped[DbColumnConstants.StandardNullableVarchar]  # Дата транзакции
    command: Mapped[
        DbColumnConstants.StandardNullableVarcharIndex
    ]  # Команда транзакции
    sum: Mapped[DbColumnConstants.StandardPrice]  # Сумма транзакции
    amount: Mapped[DbColumnConstants.StandardInteger]  # Количество

    is_failed: Mapped[DbColumnConstants.StandardBooleanFalse]  # Признак ошибки
    is_paid: Mapped[DbColumnConstants.StandardBooleanFalse]  # Признак оплаты
    is_qr_generate: Mapped[
        DbColumnConstants.StandardBooleanFalse
    ]  # Признак генерации QR

    paid_at: Mapped[DbColumnConstants.StandardNullableDateTime]  # Дата оплаты
    created_at: Mapped[DbColumnConstants.CreatedAt]  # Дата создания
    updated_at: Mapped[DbColumnConstants.UpdatedAt]  # Дата обновления

    # Relations
    order: Mapped[AppModelNames.OrderModelName] = DbRelationshipConstants.many_to_one(
        target=AppModelNames.OrderModelName,
        back_populates="kaspi_payments",
        foreign_keys=f"{AppModelNames.KaspiPaymentsModelName}.order_id",
    )

    orders: Mapped[List[AppModelNames.OrderModelName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppModelNames.OrderModelName,
            back_populates="kaspi",
            foreign_keys=f"{AppModelNames.OrderModelName}.kaspi_id",
        )
    )
