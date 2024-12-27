from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base
from app.shared.app_constants import AppModelNames, AppTableNames
from app.shared.db_constants import DbColumnConstants


class WorkshopModel(Base):
    __tablename__ = AppTableNames.WorkshopTableName
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
    factory_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.FactoryTableName, onupdate="cascade", ondelete="set null"
        )
    ]
    factory_sap_id: Mapped[DbColumnConstants.StandardVarcharIndex]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    # Relations
    # factory: Mapped[AppModelNames.FactoryModelName] = relationship(
    #     back_populates="workshops"
    # )
    # materials: Mapped[list[AppModelNames.MaterialModelName]] = relationship(
    #     back_populates="workshop"
    # )
