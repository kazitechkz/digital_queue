from sqlalchemy.orm import Mapped, relationship

from app.infrastructure.database import Base
from app.shared.app_constants import AppTableNames, AppModelNames
from app.shared.db_constants import DbColumnConstants


class MaterialModel(Base):
    __tablename__ = AppTableNames.MaterialTableName
    id: Mapped[DbColumnConstants.ID]
    title: Mapped[DbColumnConstants.StandardText]
    description: Mapped[DbColumnConstants.StandardNullableText]
    sap_id: Mapped[DbColumnConstants.StandardUniqueValue]
    status: Mapped[DbColumnConstants.StandardBooleanTrue]
    price_without_taxes: Mapped[DbColumnConstants.StandardPrice]
    price_with_taxes: Mapped[DbColumnConstants.StandardPrice]
    workshop_id: Mapped[int] = Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.WorkshopTableName, onupdate="cascade", ondelete="set null"
        )
    ]
    workshop_sap_id: Mapped[str] = Mapped[DbColumnConstants.StandardVarcharIndex]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    # Relations
    workshop: Mapped[AppModelNames.WorkshopModelName] = relationship(
        back_populates="materials"
    )
