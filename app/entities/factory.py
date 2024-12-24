from sqlalchemy.orm import Mapped, relationship

from app.infrastructure.database import Base
from app.shared.app_constants import AppTableNames, AppModelNames
from app.shared.db_constants import DbColumnConstants


class FactoryModel(Base):
    __tablename__ = AppTableNames.FactoryTableName
    id: Mapped[DbColumnConstants.ID]
    title: Mapped[DbColumnConstants.StandardText]
    description: Mapped[DbColumnConstants.StandardNullableText]
    sap_id: Mapped[DbColumnConstants.StandardUniqueValue]
    status: Mapped[DbColumnConstants.StandardBooleanTrue]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    # Relations
    workshops: Mapped[list[AppModelNames.WorkshopModelName]] = relationship(
        back_populates="factory"
    )
