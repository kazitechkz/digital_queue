from sqlalchemy.orm import Mapped

from app.infrastructure.database import Base
from app.shared.app_constants import AppTableNames
from app.shared.db_constants import DbColumnConstants


class SapRequestModel(Base):
    __tablename__ = AppTableNames.SAPRequestTableName

    id: Mapped[DbColumnConstants.ID]
    order_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.OrderTableName, onupdate="cascade", ondelete="set null"
        )
    ]
    werks: Mapped[DbColumnConstants.StandardNullableVarchar]
    matnr: Mapped[DbColumnConstants.StandardVarchar]
    kun_name: Mapped[DbColumnConstants.StandardNullableVarchar]
    iin: Mapped[DbColumnConstants.StandardNullableVarchar]
    quan: Mapped[DbColumnConstants.StandardPrice]
    price: Mapped[DbColumnConstants.StandardPrice]
    dogovor: Mapped[DbColumnConstants.StandardNullableVarchar]

    # Поля для результата операции с SAP
    status: Mapped[DbColumnConstants.StandardNullableVarchar]
    zakaz: Mapped[DbColumnConstants.StandardNullableVarcharIndex]
    text: Mapped[DbColumnConstants.StandardNullableText]
    pdf: Mapped[DbColumnConstants.StandardNullableText]
    date: Mapped[DbColumnConstants.StandardNullableDate]  # Дата переноса
    time: Mapped[DbColumnConstants.StandardNullableTime]
    # Статусы
    is_active: Mapped[DbColumnConstants.StandardBooleanTrue]
    is_failed: Mapped[DbColumnConstants.StandardBooleanFalse]
    is_paid: Mapped[DbColumnConstants.StandardBooleanFalse]

    # Даты
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
