from sqlalchemy.orm import Mapped

from app.infrastructure.database import Base
from app.shared.app_constants import AppTableNames
from app.shared.db_constants import DbColumnConstants


class KaspiPaymentModel(Base):
    __tablename__ = AppTableNames.KaspiPaymentsTableName

    id: Mapped[DbColumnConstants.ID]
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
