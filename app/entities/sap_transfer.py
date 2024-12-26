from sqlalchemy.orm import Mapped

from app.infrastructure.database import Base
from app.shared.app_constants import AppTableNames
from app.shared.db_constants import DbColumnConstants


class SAPTransferModel(Base):
    __tablename__ = AppTableNames.SAPTransferTableName

    # Уникальный идентификатор
    id: Mapped[DbColumnConstants.ID]

    # Номер заказа
    zakaz: Mapped[DbColumnConstants.StandardVarchar]  # CHAR(10)

    # Код материала в SAP
    matnr: Mapped[
        DbColumnConstants.StandardNullableVarchar
    ]  # CHAR(18), из DigitalQueue

    # Код завода
    zavod: Mapped[DbColumnConstants.StandardNullableVarchar]  # CHAR(4), из DigitalQueue

    # Код цеха
    sklad: Mapped[DbColumnConstants.StandardNullableVarchar]  # CHAR(4), из DigitalQueue

    # Объем заказа
    quan: Mapped[DbColumnConstants.StandardNullablePrice]  # NUMC(13), из DigitalQueue

    # Номер транспортного средства
    tr_nr: Mapped[DbColumnConstants.StandardNullableVarchar]  # Из DigitalQueue

    # Дата взвешивания
    date_weighted: Mapped[DbColumnConstants.StandardNullableDate]  # Из DigitalQueue

    # Время взвешивания
    time_weighted: Mapped[DbColumnConstants.StandardNullableTime]  # Из DigitalQueue

    # Статус переноса
    status: Mapped[DbColumnConstants.StandardNullableVarchar]  # CHAR(1), из SAPTransfer

    # Номер исходящей поставки
    dlvr: Mapped[DbColumnConstants.StandardNullableVarchar]  # CHAR(10), из SAPTransfer

    # Описание причины ошибочного переноса
    text: Mapped[DbColumnConstants.StandardNullableVarchar]  # CHAR(50), из SAPTransfer

    # Дата создания поставки
    date_transfer: Mapped[DbColumnConstants.StandardNullableDate]  # Из SAPTransfer

    # Время создания поставки
    time_transfer: Mapped[DbColumnConstants.StandardNullableTime]  # Из SAPTransfer

    # Таймстампы создания и обновления
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
