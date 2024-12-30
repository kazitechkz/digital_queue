from typing import List

from sqlalchemy.orm import Mapped, relationship

from app.infrastructure.database import Base
from app.shared.app_constants import AppModelNames, AppTableNames
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants


class MaterialModel(Base):
    __tablename__ = AppTableNames.MaterialTableName
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
    price_without_taxes: Mapped[DbColumnConstants.StandardPrice]
    price_with_taxes: Mapped[DbColumnConstants.StandardPrice]
    workshop_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.WorkshopTableName, onupdate="cascade", ondelete="set null"
        )
    ]
    workshop_sap_id: Mapped[DbColumnConstants.StandardVarcharIndex]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    # Relations
    file: Mapped[AppModelNames.FileModelName] = DbRelationshipConstants.many_to_one(
        target=AppModelNames.FileModelName,
        back_populates="materials",
        foreign_keys=f"{AppModelNames.MaterialModelName}.file_id",
    )
    workshop: Mapped[AppModelNames.WorkshopModelName] = (
        DbRelationshipConstants.many_to_one(
            target=AppModelNames.WorkshopModelName,
            back_populates="materials",
            foreign_keys=f"{AppModelNames.MaterialModelName}.workshop_id",
        )
    )
    orders: Mapped[List[AppModelNames.OrderModelName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppModelNames.OrderModelName,
            back_populates="material",
            foreign_keys=f"{AppModelNames.OrderModelName}.material_id",
        )
    )
