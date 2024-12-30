from typing import List

from sqlalchemy.orm import Mapped

from app.infrastructure.database import Base
from app.shared.app_constants import AppModelNames, AppTableNames
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants


class ASVUWeightModel(Base):
    __tablename__ = AppTableNames.ASVUWeightTableName

    # Уникальный идентификатор взвешивания
    id: Mapped[DbColumnConstants.ID]

    # Идентификатор взвешивания
    weighting_id: Mapped[DbColumnConstants.StandardInteger]

    # Дата взвешивания
    date_weighted: Mapped[DbColumnConstants.StandardDateTime]

    # Номер автомобиля
    car_number: Mapped[DbColumnConstants.StandardVarchar]

    # Отправитель
    sender_id: Mapped[DbColumnConstants.StandardInteger]
    sender_name: Mapped[DbColumnConstants.StandardVarchar]

    # Получатель
    receiver_id: Mapped[DbColumnConstants.StandardInteger]
    receiver_name: Mapped[DbColumnConstants.StandardVarchar]

    # SAP номер материала
    sap_mat_number: Mapped[DbColumnConstants.StandardInteger]

    # Название системы
    system_name: Mapped[DbColumnConstants.StandardVarchar]

    # Весовые данные
    gross_weight_kg: Mapped[DbColumnConstants.StandardNullablePrice]  # Вес брутто
    tare_weight: Mapped[DbColumnConstants.StandardNullablePrice]  # Вес тары
    netto_weight: Mapped[DbColumnConstants.StandardNullablePrice]  # Вес нетто

    # Описание
    description: Mapped[DbColumnConstants.StandardNullableText]

    # Счёт-фактура
    invoice_id: Mapped[DbColumnConstants.StandardNullableInteger]
    invoice_name: Mapped[DbColumnConstants.StandardNullableVarchar]

    # Получатель счёта
    invoice_receiver_id: Mapped[DbColumnConstants.StandardNullableInteger]
    invoice_receiver_name: Mapped[DbColumnConstants.StandardNullableVarchar]

    # Поставка
    supply_name: Mapped[DbColumnConstants.StandardNullableVarchar]

    # Номер карты
    card_number: Mapped[DbColumnConstants.StandardNullableVarchar]

    # Таймстампы создания и обновления
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    # Relations
    act_weights: Mapped[List[AppModelNames.ActWeightModelName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppModelNames.ActWeightModelName,
            back_populates="asvu",
        )
    )
