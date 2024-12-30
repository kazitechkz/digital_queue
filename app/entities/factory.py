from typing import List

from sqlalchemy.orm import Mapped, relationship

from app.infrastructure.database import Base
from app.shared.app_constants import AppModelNames, AppTableNames
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants


class FactoryModel(Base):
    __tablename__ = AppTableNames.FactoryTableName
    id: Mapped[DbColumnConstants.ID]
    file_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.FileTableName, onupdate="set null", ondelete="cascade"
        )
    ]
    title: Mapped[DbColumnConstants.StandardText]
    description: Mapped[DbColumnConstants.StandardNullableText]
    sap_id: Mapped[DbColumnConstants.StandardUniqueValue]
    status: Mapped[DbColumnConstants.StandardBooleanTrue]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    # Relations
    workshops: Mapped[List[AppModelNames.WorkshopModelName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppModelNames.WorkshopModelName,
            back_populates="factory",
            foreign_keys=f"{AppModelNames.WorkshopModelName}.factory_id",
        )
    )
    orders: Mapped[List[AppModelNames.OrderModelName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppModelNames.OrderModelName,
            back_populates="factory",
            foreign_keys=f"{AppModelNames.OrderModelName}.factory_id",
        )
    )
    file: Mapped[AppModelNames.FileModelName] = DbRelationshipConstants.many_to_one(
        target=AppModelNames.FileModelName,
        back_populates="factories",
        foreign_keys=f"{AppModelNames.FactoryModelName}.file_id",
    )
