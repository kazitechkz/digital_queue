from typing import List

from sqlalchemy.orm import Mapped

from app.infrastructure.database import Base
from app.shared.app_constants import AppTableNames, AppModelNames
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants


class FileModel(Base):
    __tablename__ = AppTableNames.FileTableName
    id: Mapped[DbColumnConstants.ID]
    filename: Mapped[DbColumnConstants.StandardVarchar]
    file_path: Mapped[DbColumnConstants.StandardText]
    file_size: Mapped[DbColumnConstants.StandardInteger]
    content_type: Mapped[DbColumnConstants.StandardVarchar]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    factories: Mapped[List[AppModelNames.FactoryModelName]] = DbRelationshipConstants.one_to_many(
        target=AppModelNames.FactoryModelName,
        back_populates="file",
        foreign_keys=f"{AppModelNames.FactoryModelName}.file_id"
    )
    materials: Mapped[List[AppModelNames.MaterialModelName]] = DbRelationshipConstants.one_to_many(
        target=AppModelNames.MaterialModelName,
        back_populates="file",
        foreign_keys=f"{AppModelNames.MaterialModelName}.file_id"
    )
    organizations: Mapped[List[AppModelNames.OrganizationModelName]] = DbRelationshipConstants.one_to_many(
        target=AppModelNames.OrganizationModelName,
        back_populates="file",
        foreign_keys=f"{AppModelNames.OrganizationModelName}.file_id"
    )