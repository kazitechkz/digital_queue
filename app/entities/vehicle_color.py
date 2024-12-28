from typing import List

from sqlalchemy.orm import Mapped

from app.infrastructure.database import Base
from app.shared.app_constants import AppTableNames, AppModelNames
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants


class VehicleColorModel(Base):
    __tablename__ = AppTableNames.VehicleColorTableName
    id: Mapped[DbColumnConstants.ID]
    title: Mapped[DbColumnConstants.StandardVarchar]
    value: Mapped[DbColumnConstants.StandardUniqueValue]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
    #Relationship
    vehicles: Mapped[
        List[AppModelNames.VehicleModelName]] = DbRelationshipConstants.one_to_many(
        target=AppModelNames.VehicleModelName,
        back_populates="color",
        foreign_keys=f"{AppModelNames.VehicleModelName}.color_id"
    )